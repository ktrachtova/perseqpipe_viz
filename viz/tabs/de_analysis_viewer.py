import streamlit as st
import pandas as pd
from viz import utils
from viz import settings
import re


ALLOWED_COUNTS = ['raw', 'norm', 'vst']


def read_counts_table(file):

    counts_df = pd.read_csv(file, sep='\t')

    # check 'gene' column present
    if counts_df.columns[0] != "gene":
        st.error(f"First column in loaded counts table is expected to be called 'gene' but detected name of column is {counts_df.columns[0]}")
    
    # check all columns with counts do contain in its name a suffix specifying type of counts
    sample_cols = counts_df.columns[1:]  # All except 'gene'

    # Parse the counts - check type (raw / norm / vst) and create a conditon table
    norm_dfs = {}
    sample_info = []

    for col in sample_cols:
        try:
            sample_id, norm_type, condition = col.rsplit("_", 2)
        except ValueError:
            st.error(f"Column '{col}' does not match the expected format: '<sample>_<norm>_<condition>'")

        if norm_type not in ALLOWED_COUNTS:
            st.error(f"Column '{col}' has unrecognized normalization type '{norm_type}'")

        # Add to sample metadata
        sample_info.append({
                'column': col,
                'sample': sample_id,
                'normalization': norm_type,
                'condition': condition
            })

        # Add to appropriate norm matrix
        if norm_type not in norm_dfs:
            norm_dfs[norm_type] = counts_df[['gene', col]].copy()
        else:
            norm_dfs[norm_type][col] = counts_df[col]


    # Metadata table
    metadata_df = pd.DataFrame(sample_info)

    return metadata_df, norm_dfs


def read_de_table(file):

    de_df = pd.read_csv(file, sep='\t')

    # check 'gene' column present
    if de_df.columns[0] not in ['gene', 'sequence']:
        st.error(f"First column in loaded DE table is expected to be called 'gene' (for miRNA/isomiRs) or 'sequence' (for sncRNA), but detected name of column is {de_df.columns[0]}")

    # Columns common to all comparisons -> only valied if sncRNA are being analyzed!
    common_cols = [de_df.columns[0], 'pirna', 'trna', 'snorna', 'srna', 'mrna', 'lncrna', 'MINT_plate', 'baseMean']
    present_common_cols = [c for c in common_cols if c in de_df.columns]

    # Identify comparison-specific columns using regex
    comparison_pattern = re.compile(r'^(stat|pval|padj|logFC)_(.+)$')
    comparison_dict = {}

    for col in de_df.columns:
        match = comparison_pattern.match(col)
        if match:
            metric, comparison = match.groups()
            if comparison not in comparison_dict:
                comparison_dict[comparison] = set()
            comparison_dict[comparison].add(metric)

    # Prepare dataframes for each comparison
    comparison_dfs = {}
    for comparison, metrics in comparison_dict.items():
        required_metrics = {'pval', 'padj', 'logFC'}

        missing = required_metrics - metrics

        if missing:
            print(f"Skipping '{comparison}': missing required columns: {', '.join(missing)}")
            continue

        has_stat = 'stat' in metrics
        if not has_stat:
            print(f"Note: 'stat' column is missing for comparison '{comparison}'.")

        # Build list of columns to extract
        cols_to_extract = present_common_cols + [
            f"{metric}_{comparison}" for metric in (['stat'] if has_stat else []) + list(required_metrics)
        ]
        # Create a new dataframe
        comparison_dfs[comparison] = de_df[cols_to_extract].copy()

    return comparison_dfs


def render_tab():
    st.title("DE Analysis Viewer")

    col1, col2 = st.columns(2)

    with col1:
        uploaded_de = st.file_uploader("Upload TSV file with DE results", type=["tsv"], help="Expecting file with required columns 'gene' (miRNA/isomiRs) or 'sequence' (sncRNA), 'baseMean' and then at least 4 columns containing word 'stat', 'pvalue', 'padj', and 'logFC'. Multiple such columns can be present and should contain suffix '_cond1_vs_cond2' to specify comparison or '_lrt' for specifying these are from a LRT test.")
    with col2:
        uploaded_counts = st.file_uploader("Upload TSV file with counts", type=["tsv"], help="Expecting file with first column 'gene' with miRNA/isomiR and variable number of columns with counts, one per sample. Name of ach count column should consist of sample and a suffix stating what types of counts these are ('_raw', '_norm', '_vst').")

    if uploaded_counts is not None:
        metadata_df, norm_dfs = read_counts_table(uploaded_counts)
        available_counts = list(norm_dfs.keys())

    if uploaded_de is not None:
        comparison_dfs = read_de_table(uploaded_de)

    tabA, tabB =  st.tabs(["PCA plot", "Heatmap"])

    with tabA:
        if uploaded_counts is not None:
            st.subheader("Counts overview", divider="grey")

            selected_counts = st.selectbox("Choose normalization type for analysis", options=available_counts)
            st.dataframe(norm_dfs[selected_counts])

            if selected_counts in ['norm', 'vst']:
                expression_df = norm_dfs[selected_counts]
                pca_fig = utils.plot_pca(expression_df, metadata_df, gene_column='gene')
                st.plotly_chart(pca_fig)
            else:
                st.error("PCA cannot be performed on raw counts. Please select 'norm' or 'vst'.")
    
    with tabB:
        if uploaded_de is not None and uploaded_counts is not None:
            st.subheader("Heatmap sequence selection", divider="grey")

            col1, col2 = st.columns(2)
            # PRIMARY - select comparison to visualize and normalization type --------------------------
            with col1:
                selected_comparison = st.selectbox("Choose comparison", options = comparison_dfs.keys())
            with col2:
                selected_counts_de = st.selectbox("Select normalization", options=available_counts)

            # Prepare DE table based on selected comparison
            selected_de = comparison_dfs[selected_comparison]
            # Prepare table with counts based on selected normalization type
            selected_counts_df = norm_dfs[selected_counts_de]

            # SECONDARY - select counts and filter genes based on baseMean, padj, pvalu or logFC -------
            col1, col2 = st.columns(2)
            with col1:
                logfc_col = [col for col in selected_de.columns if 'logFC' in col]
                de_logfc = st.text_input("Log2FC thresholds", value="0,0", help="Set MIN,MAX Log2FC thresholds, only sequences with log2FC < MIN and > MAX will be shown. Example: `-1,1` will only show sequences with log2FC < -1 (down-regulated) and log2FC > 1 (up-regulated).")
                pval_col = [col for col in selected_de.columns if 'pval' in col]
                de_pval = st.slider("P-value", min_value=selected_de[pval_col].min().min(), max_value=1.0, value=1.0)
            
            with col2:
                de_basemean = st.text_input("Min baseMean", value=0.0)
                padj_col = [col for col in selected_de.columns if 'padj' in col]
                de_padj = st.slider("Adjusted P-value", min_value=selected_de[padj_col].min().min(), max_value=1.0, value=1.0)

            # Filter DE dataframe based on all the above
            # Apply combined filters
            # Step 1: Filter by logFC range — keep full rows
            # Step-by-step boolean masks
            filtered_selected_de = selected_de.loc[
                ((selected_de[logfc_col[0]] <= float(de_logfc.split(",")[0])) |
                (selected_de[logfc_col[0]] >= float(de_logfc.split(",")[1]))) &
                (selected_de["baseMean"] >= float(de_basemean)) &
                (selected_de[pval_col[0]] < de_pval) &
                (selected_de[padj_col[0]] < de_padj)]
  
            st.dataframe(filtered_selected_de)

            st.subheader("Heatmap visualization", divider="grey")

            col1, col2 = st.columns(2)
            with col1:
                cluter_rows = st.toggle("Cluster rows", value = False)
                cluster_cols = st.toggle("Cluster columns", value = True)
                color_cond1 = st.text_input("Color for condition 1:", "gold")
                heatmap_palette = st.selectbox("Heatmap palette", options = settings.HEATMAP_COLORS, index = 7)

            with col2:
                gene_names = "" # Initialize variable so that we can pass it to heatmap-creating function even if user does not specify it
                show_rows = st.toggle("Show MINTplate identifiers / sequences", value = False)
                show_cols = st.toggle("Show sample names", value = True)
                color_cond2 = st.text_input("Color for condition 2:", "darkblue")
                if show_rows:
                    gene_names = st.selectbox("Row labels", options = ['MINT_plate', 'sequence'], index = 0)

            # Get list of compared conditions ['cond1','cond2']
            de_conditions = selected_comparison.split("_vs_")
            metadata_df_selected = metadata_df[metadata_df['condition'].isin(de_conditions)]
            metadata_df_selected = metadata_df_selected[metadata_df_selected['normalization'] == selected_counts_de]

            heatmap_fig = utils.create_heatmap(selected_counts_df, metadata_df_selected, filtered_selected_de, de_conditions, cluter_rows, cluster_cols, show_rows, show_cols, color_cond1, color_cond2, heatmap_palette, gene_names)

            st.pyplot(heatmap_fig.fig)
