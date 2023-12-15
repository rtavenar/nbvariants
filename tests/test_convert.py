from nbvariants import remove_corr_from_notebook, single_source_multi_output

# remove_corr_from_notebook(
#     "tests/data/UNet_corr.ipynb", 
#     "tests/output/UNet_nocorr.ipynb", 
#     tags_remove=None, 
#     tags_do_not_remove=["keep"]
# )

single_source_multi_output(
    "tests/data/UNet_source.ipynb", 
    {
        "tests/output/UNet_nocorr.ipynb": ["nocorr"],
        "tests/output/UNet_corr.ipynb": ["corr"]
    }
)