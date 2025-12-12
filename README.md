<picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/images/perseqpipe_viz_logo_light.png">
    <img alt="" src="docs/images/perseqpipe_viz_logo_dark.png" style="margin-bottom: 50px;">
</picture>

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=fff)](https://www.docker.com/)
[![PerSeqPipe](https://img.shields.io/badge/repo-PerSeqPIPE-20B2AA)](https://github.com/ktrachtova/perseqpipe)

## ⭐ Introduction

PerSeqPIPE VIZ is a Streamlit application for visualization of results from [PerSeqPIPE pipeline](https://github.com/ktrachtova/perseqpipe). 

Current version of PerSeqPIPE VIZ has 4 sections, each specializing on interactive exploration / visualization of specific data produced by PerSeqPIPE:
1. **Reads Counts Viewer**: Exploration and visualization of read statistics after each step of preprocessing in PerSeqPIPE workflow
2. **sncRNA Counts Viewer**: Exploration of sequence-centric results from PerSeqPIPE workflow
3. **DE Analysis Viewer**: Visualization of results from Differential Expression analysis, including PCA plot and interactive heatmaps
4. **Reads Coordinate Extraction**: Extract information about specific read sequence, such as coordinates for visualization in [IGV tool](https://igv.org/), mismatches, strand etc.

For more information about each section, go to [Sections documentation](docs/sections.md).

## 💻 Usage

### Quick start (local environment)

First download the repository code locally. 
```
git pull https://github.com/ktrachtova/perseqpipe_viz.git
```

Then install prerequisities stated in file [prerequisites](requirements.txt). Finally run following command:

```
streamlit run app.py
```

This will start the application in a your default web-browser. 

### Quick start (using Docker)

If you do not have or do not want to install all prerequisites you can also use publicly available docker image with all dependencies already installed. 

```
# For linux/amd64 infrastructure
docker pull ktrachtok/perseqpipe_viz:amd64-1.0
docker run -p 8502:8502 ktrachtok/perseqpipe_viz:amd64-1.0

# For arm infrastructure
docker pull ktrachtok/perseqpipe_viz:arm64-1.0
docker run -p 8502:8502 ktrachtok/perseqpipe_viz:arm64-1.0
```

This will start the PerSeqPIPE VIZ at `http://0.0.0.0:8502` (when running through docker, the web browser will not automatically open, it must be started by the user). The application will be available after this message appears in the terminal:
```
You can now view your Streamlit app in your browser.

URL: http://0.0.0.0:8502
```

The port `8502` can be changed to whichever port is available using variable `PORT`.
```
docker run -e PORT=8501 -p 8501:8501 ktrachtok/perseqpipe_viz:arm64-1.0
```

## 📥 Inputs

Inputs for the PerSeqPIPE VIZ are various files produced by the PerSeqPIPE workflow.

| Tab                  | Input file(s)                          |
|----------------------|----------------------------------------|
| Reads Counts Viewer  | `read_counts_summary.csv`              |
| sncRNA Counts Viewer | `{sample}.genome.short_rna_counts.tsv` |
| DE Analysis Viewer   | `DE_analysis_[isomirs\|mirna\|sncrna]_results.tsv`, `DE_analysis_[isomirs\|mirna\|sncrna]_counts.tsv` |
| Reads Coordinate Extraction | `{sample}.genome.Aligned.sortedByCoord.out.bam` |

For description of each input file, please got to [PerSeqPIPE VIZ Sections](docs/sections.md).

### Providing inputs from different tools

As long as an input file for specific part of PerSeqPIPE is following requirement format (columns, type of data etc.) then PerSePIPE VIZ will be able to work with it. If you want to visualize data obtained elsewhere, we recommend to inspect  [example inputs](test_data/) for the PerSeqPIPE VIZ and copy the format. 

