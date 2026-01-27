<picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/images/perseqpipe_viz_logo_light.png">
    <img alt="" src="docs/images/perseqpipe_viz_logo_dark.png" style="margin-bottom: 50px;">
</picture>

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=fff)](https://www.docker.com/)
[![PerSeqPipe](https://img.shields.io/badge/repo-PerSeqPIPE-20B2AA)](https://github.com/ktrachtova/perseqpipe)

## ⭐ Introduction

PerSeqPIPE VIZ is a user-friendly application for visualization of results from [PerSeqPIPE pipeline](https://github.com/ktrachtova/perseqpipe), built using Streamlit library. 

Current version of PerSeqPIPE VIZ has 4 sections, each specializing in interactive exploration and visualization of specific data produced by PerSeqPIPE:
1. **Reads Counts Viewer**: Exploration and visualization of read statistics after each step of preprocessing in the PerSeqPIPE workflow
2. **sncRNA Counts Viewer**: Exploration of sequence-centric results from PerSeqPIPE workflow
3. **DE Analysis Viewer**: Visualization of results from differential dxpression (DE) analysis, including PCA plot and interactive heatmaps
4. **Reads Coordinate Extraction**: Extract information about specific read sequences, such as coordinates for visualization in the [IGV tool](https://igv.org/), mismatches, strand etc.

For more information about each section, see the [Sections documentation](docs/sections.md).

## 💻 Usage

### Quick start (local environment)

First, download the repository code locally. 
```
git clone https://github.com/ktrachtova/perseqpipe_viz.git
```

Next, install prerequisities stated in [requirements](requirements.txt). Finally, run the following command:

```
streamlit run app.py
```

This will automnatically open the application in a your default web browser. 

### Quick start (using Docker)

Alternatively, we provide publicly available Docker image with all dependencies already installed. To run PerSeqPIPE VIZ using docker, execute the following code:

```
# For linux/amd64 infrastructure
docker pull ktrachtok/perseqpipe_viz:amd64-1.0
docker run -p 8502:8502 ktrachtok/perseqpipe_viz:amd64-1.0

# For arm infrastructure
docker pull ktrachtok/perseqpipe_viz:arm64-1.0
docker run -p 8502:8502 ktrachtok/perseqpipe_viz:arm64-1.0
```
This will start the PerSeqPIPE VIZ at `http://0.0.0.0:8502`. When running through Docker, the web browser will not automatically open and must be started by the user. The application will be available after the following message appears in the terminal:
```
You can now view your Streamlit app in your browser.

URL: http://0.0.0.0:8502
```

The port `8502` can be changed to any available port using the `PORT` environment variable.
```
docker run -e PORT=8501 -p 8501:8501 ktrachtok/perseqpipe_viz:arm64-1.0
```

## 📥 Inputs

Inputs for the PerSeqPIPE VIZ are various files produced by the PerSeqPIPE workflow. Here is the overview of which files are required for which section of the PerSeqPIPE VIZ application.

| Tab                  | Input file(s)                          |
|----------------------|----------------------------------------|
| Reads Counts Viewer  | `read_counts_summary.csv`              |
| sncRNA Counts Viewer | `{sample}.genome.short_rna_counts.tsv` |
| DE Analysis Viewer   | `DE_analysis_[isomirs\|mirna\|sncrna]_results.tsv`, `DE_analysis_[isomirs\|mirna\|sncrna]_counts.tsv` |
| Reads Coordinate Extraction | `{sample}.genome.Aligned.sortedByCoord.out.bam` |

For description of each input file and its location withing PerSeqPIPE results, please got to [PerSeqPIPE VIZ Sections](docs/sections.md).

### Providing inputs from different tools

As long as an input file for a specific section of PerSeqPIPE VIZ follows required format (columns, data types, etc.), then PerSePIPE VIZ will be able to work with it. If you want to visualize data obtained elsewhere, we recommend to inspect  [example inputs](test_data/) we provide and copy their format (column names, separators etc.). 

## 🎺 Credits

PerSeqPIPE VIZ application is written and maintaned by Karolina Trachtova (karolina.trachtova@ceitec.muni.cz).

## ⁉️ Support

In case of question, found bugs or suggestions for improvement please open new issue [here](https://github.com/ktrachtova/perseqpipe_viz/issues).