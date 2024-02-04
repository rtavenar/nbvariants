import nbformat
from copy import deepcopy

def remove_corr_from_notebook(input_fname, 
                              output_fname, 
                              tags_remove=None, 
                              tags_do_not_remove=None):
    """Write a notebook that is a copy of the input 
    notebook except that code cells are made empty.

    Some exceptions exist:

    * A code cell that has a tag in the list 
      `tags_do_not_remove` is not changed
    * A markdown cell that has a tag in the list 
      `tags_remove` is made empty

    Example
    ---
    >>> remove_corr_from_notebook(path_to_input_nb, 
    ...                           path_to_output_nb, 
    ...                           tags_do_not_remove=["keep"])
    """
    if tags_do_not_remove is None:
        tags_do_not_remove = []
    if tags_remove is None:
        tags_remove = []
    
    nb = nbformat.read(input_fname, as_version=nbformat.NO_CONVERT)

    for c in nb.cells:
        do_not_remove = False
        for t in tags_do_not_remove:
            if t in c["metadata"].get("tags", []):
                do_not_remove = True
                break
        remove_anyway = False
        for t in tags_remove:
            if t in c["metadata"].get("tags", []):
                remove_anyway = True
                break
        if not do_not_remove and (c["cell_type"] == "code" or remove_anyway):
            c["source"] = ""
            c["outputs"] = ""

    nbformat.write(nb, output_fname, version=nbformat.NO_CONVERT)

def single_source_multi_output(input_fname,
                               tags_per_output, 
                               remove_listed_tags=True,
                               remove_all_outputs=False):
    """tags_per_output is a dict which keys are output 
    file names and values are the lists of tags to keep
    for the given output.
    """
    
    nb = nbformat.read(input_fname, as_version=nbformat.NO_CONVERT)

    all_tags = []
    for t in tags_per_output.values():
        all_tags.extend(t)
    all_tags = list(set(all_tags))

    for fname_output, tags_do_not_remove in tags_per_output.items():
        output_nb = nbformat.from_dict(deepcopy(nb))
        output_nb["cells"] = []
        
        for c_ in nb.cells:
            do_not_remove = False
            c = deepcopy(c_)
            for t in tags_do_not_remove:
                if t in c["metadata"].get("tags", []):
                    do_not_remove = True
                    break
            if not do_not_remove and c["cell_type"] == "code":
                c["source"] = ""
                c["outputs"] = ""
            if remove_all_outputs:
                c["outputs"] = ""
            c["metadata"]["tags"] = [t for t in c["metadata"].get("tags", [])
                                     if t not in all_tags or not remove_listed_tags]
            output_nb["cells"].append(nbformat.from_dict(c))

        nbformat.write(output_nb, fname_output, version=nbformat.NO_CONVERT)