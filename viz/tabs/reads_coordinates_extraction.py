from Bio.Seq import Seq  # for reverse complement
import pysam
import os
import streamlit as st
import plotly.express as px
import pandas as pd
import tempfile
import re

from viz.tabs import *
from viz import utils
from viz import settings


def render_tab():

    st.title("Reads Coordinate Exctraction")

    # Upload a file
    bam_file = st.file_uploader(
        "Upload a BAM file",
        type=["bam"],
        key='bam',
        help="BAM file from alignment of reads to the genome."
    )

    if bam_file is not None:
        read_seq = st.text_input("Read sequence", value="")

        if read_seq != "":

            if utils.is_valid_dna_sequence(read_seq):
                # Obtain reversed sequence as well
                rev_query_seq = str(Seq(read_seq).reverse_complement())

                # --- Save uploaded BAM to a temp file ---
                with tempfile.NamedTemporaryFile(delete=False, suffix=".bam") as tmp_bam:
                    tmp_bam.write(bam_file.read())
                    tmp_bam_path = tmp_bam.name

                matches = []
                with pysam.AlignmentFile(tmp_bam_path, "rb") as bam:
                    for read in bam:
                        read_seq_upper = read.query_sequence.upper()
                        if read_seq_upper == read_seq.upper() or read_seq_upper == rev_query_seq:
                            chrom = bam.get_reference_name(read.reference_id)
                            start = read.reference_start + 1
                            strand = "-" if read.is_reverse else "+"

                            # Extract optional tags safely
                            def get_tag_safe(tag):
                                try:
                                    return read.get_tag(tag)
                                except KeyError:
                                    return None
                
                            matches.append({
                                "Read name": read.query_name,
                                "Chromosome": chrom,
                                "Position": start,
                                "Streand": strand,
                                "NH": get_tag_safe("NH"),  # number of reported alignments
                                "HI": get_tag_safe("HI"),  # hit index
                                "AS": get_tag_safe("AS"),  # alignment score
                                "NM": get_tag_safe("NM"),  # edit distance
                                "MD": get_tag_safe("MD"),  # mismatch string
                            })

                # Clean up temporary file
                os.remove(tmp_bam_path)

                if matches:
                    df = pd.DataFrame(matches)
                    st.success(f"Found {len(df)} positions!")
                    st.dataframe(df, width='stretch')

                    # Simple genome position scatterplot
                    fig = px.scatter(
                        df,
                        x="Position",
                        y="Chromosome",
                        title="Read Positions in Genome",
                        labels={"Position": "Genomic Start Position", "Chromosome": "Chromosome"},
                        template="plotly_white"
                    )

                    st.plotly_chart(fig)

                else:
                    st.warning("No matching reads found.")
            else:
                st.error("Input sequence is not valid nucleotide sequence! Only A/C/T/G characters allowed (can be lowercase).")

