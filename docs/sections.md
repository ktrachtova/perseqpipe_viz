# PerSeqPIPE VIZ Tabs

## Table of Contents

- [PerSeqPIPE VIZ Tabs](#perseqpipe-viz-tabs)
  - [Reads Statistics Viewer](#1️⃣-reads-statistics-viewer)
    - [Input](#input)
    - [Subsection: Reads table](#subsection-reads-table)
    - [Subsection: Reads Statistics Visualization](#subsection-reads-statistics-visualization)
    - [Downloading plots](#downloading-plots)
  - [sncRNA Counts Viewer](#2️⃣-sncrna-counts-viewer)
    - [Input](#input-1)
    - [Overview](#overview)
    - [Loci-specific names](#loci-specific-names)
  - [DE Analysis Viewer](#3️⃣-de-analysis-viewer)
    - [Input](#input-2)
    - [Overview](#overview-1)
    - [PCA plot](#pca-plot)
    - [Heatmap](#heatmap)
  - [Reads Coordinate Extraction](#4️⃣-reads-coordinate-extraction)
    - [Input](#input-3)
    - [Overview](#overview-2)
    - [Example usage](#example-usage)

## 1️⃣ Reads Statistics Viewer

### Input

| input file                | location in PerSeqPIPE results |
|---------------------------|--------------------------------|
| `read_counts_summary.csv` | `{project_name}/all_stats/`    |

For description of individual columns from the `read_counts_summary.csv` please go to documentation of PerSeqPIPE [here](https://github.com/ktrachtova/perseqpipe/blob/main/docs/outputs.md#reads-statistics).

Custom CSV/TSV file (comma or tab separated) can be used as an input as long as it comply with following requirements:
* first column is `sample`
* other columns contain either read counts or percentages
* name of a column with percentage has to end with string "_%"

### Reads table

**Reads Table** provides visualization of the read counts summary CSV file created by the PerSeqPIPE workflow called `read_counts_summary.csv`. This file contains summary for number of reads passing each preprocessing and quantification step.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="images/reads_statistics_viewer/reads_table.png">
  <img src="images/reads_statistics_viewer/reads_table.png" alt="Reads table"
       style="width:600px; margin-bottom:10px;">
</picture>

### Reads Statistics Visualization

Currently supported plot types:

* **barplot** of both number of reads and % passing each preprocessing and quantification step
* **pieplot** showing % of reads in after each preprocessing and quantification step for individual samples

For **barplots**, user can adjust several features such as bar labels, setting identical y-axis range for all plots or changing colors for preprocessing steps. It is also possible to remove specific sample(s) from barplots.

For **pieplots** user can change color palette and remove specific step(s) from the pieplot. To remove specific step just click on it in the pieplot legend and all percentages shown will be automatically adjusted.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="images/reads_statistics_viewer/barplots.png">
  <img src="images/reads_statistics_viewer/barplots.png" alt="Reads table"
       style="width:600px; margin-bottom:20px;">
</picture>

### Downloading plots

All plots currently viewed (and any adjustments made by user) can be downloaded either individually (top right corner of each plot) or in a batch using button at the bottom of the Reads Statistics Viewer section. Currently supported format for batch download of all visualized plots is HTML.

## 2️⃣ sncRNA Counts Viewer

### Input

| input file                             | location in PerSeqPIPE results                     |
|----------------------------------------|----------------------------------------------------|
| `{sample}.genome.short_rna_counts.tsv` | `{project_name}/rna_quantification/genome/counts/` |

The input table format is in detail described [here](https://github.com/ktrachtova/perseqpipe/blob/main/docs/outputs.md#sncrna-quantification-output-file-format).


### Overview

This tab supports exploration of sncRNA counts produced by SNCRNA_QUANTICATION module of [PerSeqPIPE](https://github.com/ktrachtova/perseqpipe/blob/main/docs/module_description.md#module-5%EF%B8%8F%E2%83%A3-other-sncrna-quantification) for individual samples and includes following filtering:

* selecting specific sncRNA cathegory
* selecting sequences of specific length
* selecting sequences based on number of genomic alignments
* filtering based on expression
* filtering based on sequence
* filtering based on assigned feature(s)

Additionally, it is possible to obtain list of unique loci-specific gene names as well as list of unique gene names for a set of currently viewed sequences. 

### Loci-specific names

If a specific RNA can be aligned to multiple loci in genome (like many tRNA and piRNA), such gene/transcript name has suffix `_loc{x}` in the custom sncRNA GTF file used for sncRNA quantification by PerSeqPIPE. For more information, please refer to section [sncRNA GTF file format specification](https://github.com/ktrachtova/perseqpipe/blob/main/docs/outputs.md#sncrna-quantification-output-file-format) section of PerSeqPIPE documentation. 

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="images/sncrna_counts_viewer/sncrna_counts_viewer.png">
  <img src="images/sncrna_counts_viewer/sncrna_counts_viewer.png" alt="Reads table"
       style="width:600px; margin-bottom:20px;">
</picture>

## 3️⃣ DE Analysis Viewer

### Input

| input file                                       | location in PerSeqPIPE results                     |
|--------------------------------------------------|----------------------------------------------------|
| `DE_analysis_{sncrna\|mirna\|isomirs}_results.tsv` | `{project_name}/de_analysis/sncrna` or `{project_name}/de_analysis/mnirna_isomirs` |
| `DE_analysis_{sncrna\|mirna\|isomirs}_counts.tsv` | `{project_name}/de_analysis/sncrna` or `{project_name}/de_analysis/mnirna_isomirs` |

### Overview

The DE Analysis Viewer required following files:

* DE statistics table (`DE_analysis_sncrna_results.tsv` or `DE_analysis_mirna|isomirs_results.tsv` produced by DE_ANALYSIS module of PerSeqPIPE)
* table with counts (`DE_analysis_sncrna_counts.tsv` or `DE_analysis_mirna|isomirs_counts.tsv`).

Please see [PerSeqPIPE documentation](https://github.com/ktrachtova/perseqpipe/blob/main/docs/de_analysis.md#output-files) decribing these specific files and their format.

The DE Analysis Viewer has 2 separate subtabs showing interactive PCA plot and heatmap.

### PCA plot

By default, a table showing raw counts will be rendered after the input files are uploaded. 

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="images/de_analysis_viewer/pca_plot_table.png">
  <img src="images/de_analysis_viewer/pca_plot_table.png" alt="Reads table"
       style="width:600px; margin-bottom:20px;">
</picture>

PCA plot will be rendered if **VST** or **DESeq2-normalized counts** are selected. User can adjust color for conditions, point size, font size for both axes, tick labels, legend and title. 

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="images/de_analysis_viewer/pca_plot.png">
  <img src="images/de_analysis_viewer/pca_plot.png" alt="Reads table"
       style="width:600px; margin-bottom:20px;">
</picture>

### Heatmap

First subsection called **Heatmap sequence selection** allow users to filter genes/sequences for heatmap based on **log2FC thresholds**, **baseMean**, **p-value** and **adjusted p-value**. User can also switch between different pairwise comparisons (if more than 2 conditions were present inside the design file for DE Analysis) and between different normalization types (raw, VST, DESeq2-normalized).

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="images/de_analysis_viewer/heatmap_seq_selection.png">
  <img src="images/de_analysis_viewer/heatmap_seq_selection.png" alt="Reads table"
       style="width:600px; margin-bottom:20px;">
</picture>

Sequences selected through **Heatmap sequence selection** subsection are visualize in **Heatmap appearance** subsection. Here, user can adjust clustering of both rows and columns, whether to show row/column labels, their font size etc. For row labels, if miRNA or isomiRs results are being visualized then their names will be automatically shown. For sncRNA sequences, upon clicking on Show row identifiers toggle a new option will appear to select whether to show sequences or MINT plates are row labels. 

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="images/de_analysis_viewer/heatmap.png">
  <img src="images/de_analysis_viewer/heatmap.png" alt="Reads table"
       style="width:600px; margin-bottom:20px;">
</picture>

## 4️⃣ Reads Coordinate Extraction

### Input

| input file                                       | location in PerSeqPIPE results                     |
|--------------------------------------------------|----------------------------------------------------|
| `{sample}.genome.Aligned.sortedByCoord.out.bam` | `{project_name}/rna_quantification/genome/star_genome` |

### Overview

This tab provides a simple way how to quickly obtain all coordinates of specific quantified sequence. Input is a BAM file generated by PerSeqPIPE workflow (location `{project_name}/rna_quantification/genome/star_genome`) and a specific sequence of interest. Input BAM file will be searched for alignment loci of the specific sequence (on both strands) if there is any. Table summarizing all the found loci as well as a simple scatter plot summarizing on which chromosome can the sequence be found is shown.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="images/reads_coordinate_extraction/reads_coordinate_extraction.png">
  <img src="images/reads_coordinate_extraction/reads_coordinate_extraction.png" alt="Reads table"
       style="width:600px; margin-bottom:20px;">
</picture>


<picture>
  <source media="(prefers-color-scheme: dark)" srcset="images/reads_coordinate_extraction/chromosome_composition.png">
  <img src="images/reads_coordinate_extraction/chromosome_composition.png" alt="Reads table"
       style="width:600px; margin-bottom:20px;">
</picture>

### Example usage

Sequence `GCCGTGATCGTATAGTGGTTAGTACTCTGCGTT` was found as the top DE sequence with several annotations including piRNA and tRNA. We want to find out genomic loci for this sequence for a specific sample, because we want to explore how precisely does this sequence overlap each reported annotation.