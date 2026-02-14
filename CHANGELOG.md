# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] – 2026-09-02

### Added

* First public release of PerSeqPIPE VIZ, a Streamlit-based application for visualizing PerSeqPIPE results.
* Four interactive modules:
    * Reads Counts Viewer
    * sncRNA Counts Viewer
    * DE Analysis Viewer (PCA plots and heatmaps)
    * Reads Coordinate Extraction with IGV-compatible output
* Support for PerSeqPIPE output files and compatible external inputs
* Docker images for linux/amd64 and arm64 architectures
* Configurable application port via PORT environment variable
* Basic documentation and example input files