
import zipfile
import io
import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt


from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from matplotlib.patches import Patch
from viz.settings import HEATMAP_COLORS
import plotly.io as pio

pio.kaleido.scope.mathjax = None


def safe_read_table(uploaded_file, index_col=None, file_description="uploaded file"):
    """Safely reads a CSV or TSV file by attempting to auto-detect the delimiter."""
    try:
        # Try comma first
        df = pd.read_csv(uploaded_file, sep=",", index_col=index_col)
        
        # If only one column was parsed, maybe it's tab-separated
        if len(df.columns) == 1:
            uploaded_file.seek(0)  # Reset file pointer
            df = pd.read_csv(uploaded_file, sep="\t", index_col=index_col)

        if df.empty:
            st.warning(f"⚠️ {file_description} is empty or only contains header.")
            return None

        return df

    except pd.errors.EmptyDataError:
        st.error(f"❌ {file_description} appears to be completely empty.")
    except pd.errors.ParserError:
        st.error(f"❌ {file_description} could not be parsed. Check the file format (CSV or TSV).")
    except Exception as e:
        st.error(f"❌ Unexpected error reading {file_description}: {e}")

    return None


# Function to create bar plots
def plot_bar_chart(df, category, color, y_axis_range, columns_to_render, text_bars = False, remove_samples = None):
    # Create yaxis label text based on whether we visualize counts or %
    if columns_to_render == "counts":
        yaxis_label = "read counts"
    else:
        yaxis_label = "read %"

    # Remove samples
    df_filtered = df[~df["sample"].isin(remove_samples)]

    if text_bars:
        fig = px.bar(df_filtered, x='sample', y=category, title=f"{category}", 
                    labels={category: yaxis_label, "Sample": "Sample"}, 
                    height=500,
                    text_auto='.2s',
                    color_discrete_sequence=[color]
        )
        fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)

    else:
        fig = px.bar(df_filtered, x='sample', y=category, title=f"{category}", 
                    labels={category: yaxis_label, "Sample": "Sample"}, 
                    height=500,
                    color_discrete_sequence=[color]
        )
    if y_axis_range:
        fig.update_yaxes(range=y_axis_range)  # Set uniform y-axis range

    #fig.update_layout(xaxis_tickangle=-90, showlegend=False)
    max_label_len = max(df_filtered["sample"].astype(str).map(len))
    bottom_margin = min(300, 100 + max_label_len * 6)  # cap at 300

    fig.update_layout(
    xaxis_tickangle=-90,  # or -90 if you prefer vertical
    margin=dict(b=bottom_margin),   # increase bottom margin so labels don’t overlap title
    title_x=0.5  # keep title centered
    )

    fig.update_coloraxes(showscale=False)

    return fig


def plot_pie_plot(df, columns_to_plot):
    # Generate pie charts
    figs = []
    for _, row in df.iterrows():
        sample_name = row["sample"]
        raw_reads = row["raw_reads"]
        
        # Create a dictionary with category names and their percentage of raw_reads
        percentages = {col: (row[col] / raw_reads) * 100 for col in columns_to_plot}
        
        # Create a Pie chart
        fig = px.pie(
            names=percentages.keys(),
            values=percentages.values(),
            title=f"Read Distribution for {sample_name}"
        )
        figs.append(fig)
    return figs


def get_unique_gene_names(df):
    # Extract and collect unique gene names
    gene_columns = ['pirna', 'trna', 'snorna', 'srna', 'mrna', 'lncrna']
    unique_genes = set()  # Use a set to store unique gene names

    for col in gene_columns:
        if col in df.columns:
            df[col] = df[col].astype(str).fillna("")  # Ensure strings and fill NaNs
            for values in df[col]:
                unique_genes.update(values.split(','))  # Split by ',' and add to the set

    unique_genes.discard('')
    unique_genes.discard('nan')
    # Convert to a DataFrame for display
    unique_genes_df = pd.DataFrame(sorted(unique_genes), columns=["Unique Gene Names"])
    return unique_genes_df


def create_heatmap(norm_counts, design_df, de_results_df, de_conditions, cluter_rows, cluter_cols, show_rows, show_cols, color_cond1, color_cond2, heatmap_palette, gene_names):
    #filtered_design_df = design_df[design_df['condition'].isin(de_conditions)]
    # Select top variable genes
    norm_counts_filtered = norm_counts[["gene"] + list(design_df['column'])]
    top_genes = de_results_df[de_results_df.columns[0]].tolist()
    heatmap_data = norm_counts_filtered[norm_counts_filtered["gene"].isin(top_genes)]
    # Check what should be row labels
    if gene_names == "MINT_plate":
        gene_names_df = de_results_df[['sequence', 'MINT_plate']]
        # Merge df1 with df2 (left join keeps all rows from df1)
        merged = heatmap_data.merge(gene_names_df, left_on="gene", right_on="sequence", how="left")
        # Replace gene with MINT_plate
        merged = merged.drop(columns=["gene", "sequence"]).rename(columns={"MINT_plate": "gene"})
        heatmap_data = merged

    # Map annotation column to colors
    # palette = sns.color_palette("Set2", len(de_conditions))
    palette = [color_cond1, color_cond2]
    lut = dict(zip(de_conditions, palette))
    # Ensure the correct mapping and column order
    col_colors = pd.DataFrame(
        design_df.set_index('column')['condition'].map(lut),
        columns=['condition']
    )
    heatmap_data = heatmap_data.reset_index(drop=True).set_index("gene")
    # Z-score scaling across rows (genes) like `scale="row"`
    scaler = StandardScaler()
    zscore_data = pd.DataFrame(
        scaler.fit_transform(heatmap_data.T).T,
        index=heatmap_data.index,
        columns=heatmap_data.columns
    )

    # Create clustermap
    sns.set(font_scale=1.0)
    g = sns.clustermap(
        zscore_data,
        cmap=heatmap_palette,
        col_cluster=cluter_cols,
        row_cluster=cluter_rows,
        col_colors=col_colors,
        figsize=(10, 10),
        xticklabels=show_cols,
        yticklabels=show_rows
    )

    # Is row names enabled, rotate them so they are horizontal not vertical
    if show_rows:
        g.ax_heatmap.set_yticklabels(g.ax_heatmap.get_yticklabels(), rotation=0)


    if g.ax_col_dendrogram.legend_:
        g.ax_col_dendrogram.legend_.remove()

    handles = [Patch(facecolor=lut[cond], label=cond) for cond in de_conditions]

    g.fig.legend(
    handles=handles,
    title="condition",
    loc="upper left",
    bbox_to_anchor=(1.0, 1.0),
    frameon=False,
    prop={'size':16},
    title_fontsize=18
    )

    return g


def create_images(figure):
    # PNG
    buf_png = io.BytesIO()
    figure.fig.savefig(buf_png, format="png", bbox_inches="tight")
    buf_png.seek(0)

    # SVG
    buf_svg = io.BytesIO()
    figure.fig.savefig(buf_svg, format="svg", bbox_inches="tight")
    buf_svg.seek(0)

    # PDF
    buf_pdf = io.BytesIO()
    figure.fig.savefig(buf_pdf, format="pdf", bbox_inches="tight")
    buf_pdf.seek(0)

    return buf_png, buf_svg, buf_pdf


def create_boxplot(plot_df, selected_gene, condition_colors):
    """
    """
    sns.set_style("white")  # Use "white" for no gridlines
    sns.set_context("notebook", font_scale=1.4)  # Larger fonts

    # Plot
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.boxplot(
        data=plot_df,
        x='condition',
        y='expression',
        palette=condition_colors,
        ax=ax,
        width=0.4  # Default is 0.8; lower = thinner
    )
    strip = sns.stripplot(
        data=plot_df,
        x='condition',
        y='expression',
        color='grey',
        size=10,
        jitter=True,
        dodge=True,
        ax=ax
    )

    # Modify dots: hollow + alpha
    for collection in strip.collections:
        collection.set_facecolor((0, 0, 0, 0.5))  # light grey with alpha
        collection.set_edgecolor("black")
        collection.set_linewidth(1.0)

    ax.set_title(f"Expression of {selected_gene}")
    ax.set_ylabel("Normalized Expression")
    ax.set_xlabel("Condition")
    # Remove gridlines manually (if any)
    ax.grid(False)

    # Keep left and bottom borders (axes), remove top/right
    fig.tight_layout()

    return fig, ax


def plot_pca(expression_df: pd.DataFrame, metadata_df: pd.DataFrame, gene_column: str = "gene") -> None:
    """
    Plot an interactive PCA using Plotly based on a normalized expression DataFrame.

    Parameters:
    - expression_df: DataFrame with genes as rows and sample columns, including the gene identifier column
    - metadata_df: DataFrame with columns: ['column', 'sample', 'normalization', 'condition']
    - gene_column: Name of the gene identifier column (default: 'gene')
    """
    # Transpose and prepare expression matrix
    expr = expression_df.set_index(gene_column).T  # samples as rows
    expr.index.name = 'column'
    
    # Merge with metadata
    merged = pd.merge(expr, metadata_df, on='column')
    features = merged.drop(columns=['column', 'sample', 'normalization', 'condition'])
    metadata = merged[['sample', 'condition']]

    # Standardize features and run PCA
    scaled = StandardScaler().fit_transform(features)
    pca = PCA(n_components=2)
    pca_result = pca.fit_transform(scaled)

    # Prepare PCA results DataFrame
    pca_df = pd.DataFrame(pca_result, columns=["PC1", "PC2"])
    pca_df["sample"] = metadata["sample"].values
    pca_df["condition"] = metadata["condition"].values
    var1, var2 = pca.explained_variance_ratio_[:2] * 100

    # Plot using Plotly
    fig = px.scatter(
        pca_df,
        x="PC1",
        y="PC2",
        color="condition",
        hover_name="sample",
        title=f"PCA of normalized counts (PC1: {var1:.1f}%, PC2: {var2:.1f}%)",
        width=900,
        height=600
    )
    fig.update_traces(marker=dict(size=10, line=dict(width=1)))

    return fig


# Generate ZIP of all HTML plots (cached)
def generate_zip(plot_dict, type):
    if type == "html":
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for title, html_content in plot_dict.items():
                zip_file.writestr(f"{title}.html", html_content)
        zip_buffer.seek(0)
        return zip_buffer
    elif type == "pdf":
        zip_buffer_pdf = io.BytesIO()
        with zipfile.ZipFile(zip_buffer_pdf, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for title, fig in plot_dict.items():
                # Convert Plotly figure to PDF
                pdf_bytes = pio.to_image(fig, format="pdf")
                # Write PDF to ZIP file
                zip_file.writestr(f"{title}.pdf", pdf_bytes)
        zip_buffer_pdf.seek(0)
        return zip_buffer_pdf
    elif type == "png":
        zip_buffer_png = io.BytesIO()
        with zipfile.ZipFile(zip_buffer_png, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for title, fig in plot_dict.items():
                # Convert Plotly figure to PNG
                png_bytes = pio.to_image(fig, format="png", engine='orca')
                # Write PNG to ZIP file
                zip_file.writestr(f"{title}.png", png_bytes)
        zip_buffer_png.seek(0)    
        return zip_buffer_png
