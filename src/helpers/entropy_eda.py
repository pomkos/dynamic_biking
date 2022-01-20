import streamlit as st
import pandas as pd


def format_options(option: str) -> str:
    """
    Formats options for presentation in streamlit
    """
    return option.title()


def grapher(x, y, data, graph, color, out_path, save=False):
    """
    Uses seaborn to create the requested graph
    """
    import seaborn as sns
    import matplotlib.pyplot as plt

    graph = graph.strip("plot").strip()
    if 'facet' in graph:
        st.error("Not yet supported")
        st.stop()
    if ("bar" in graph) | ("box" in graph):
        g = sns.catplot(x=x, y=y, data=data, kind=graph, hue=color)
        plt.xticks(rotation=45, horizontalalignment="right")

    if "scatter" in graph:
        g = sns.relplot(x=x, y=y, data=data, kind=graph, hue=color)

    plt.title(f"{format_options(x)} vs {format_options(y)}")
    plt.xlabel(format_options(x))
    plt.ylabel(format_options(y))

    if save:
        g.savefig(f"{out_path}/{graph}_{x}_v_{y}.png", dpi=300)
    return g


def read_entropy_df(filename: str, out_path: str) -> pd.DataFrame:
    """
    Reads in excel file, splits ID column in ID and session
    """
    try:
        df = pd.read_excel(f"{out_path}/{filename}")
        tag = df["ID"].str.split("_", expand=True)
        tag.columns = ["participant", "session"]
        df = pd.concat([df, tag], axis=1).rename({"ID": "id_sess"}, axis=1)
        part_info = ["participant", "session", "id_sess"]
        df = df[
            part_info + [col for col in df.columns if col not in part_info]
        ]  # reorganize
        return df
    except:
        st.error(f"{filename} not found in the output folder")
        st.stop()


def app(filename: str, out_path:str):
    """
    Helps create some simple graphs using the entropies.xls file created by the MatLab script.
    """
    from helpers import helper_functions as h

    df_ent = read_entropy_df(filename, out_path) # entropy df
    df_sess = pd.read_excel(f'{out_path}/session_info.xls') # session info df
    df_sess = df_sess.astype({
        'participant':str,
        'session':str,
        'id_sess':str,
        'mode':str,
    })
    
    df = df_sess.merge(df_ent, suffixes=('_step2','_matlab'))
    st.info(f'The table below was created by merging the file created in Step 2 and "{filename}"')
    st.write(df)

    st.write("## Graphing")
    graph_options = ["bar plot", "box plot", "scatterplot", "facet grid"]
    cat_options = ['participant', 'session', 'id_sess', 'mode' , 'speed', 'stiffness'] # categorical variables
    num_options = [col for col in df.columns if col not in cat_options] # numerical variables
    num_options.sort()

    all_options = cat_options + num_options
    
    color_options = ['Nothing'] + cat_options

    colx, coly = st.columns(2)

    with colx:
        x = st.selectbox("X axis", options=all_options, format_func=format_options, index=1)
    with coly:
        y = st.selectbox(
            "Y axis", options=all_options, format_func=format_options, index=6
        )

    hue = st.selectbox("Color by", options=color_options, format_func=format_options)
    if hue == 'Nothing':
        hue = None

    if df[x].dtype == "O":
        # if selected column is string/object, barplot is default
        default = 0
    else:
        # if selected column is not string/object, scatterplot is default
        default = 2

    graph = st.selectbox(
        "Graph type", options=graph_options, index=default, format_func=format_options
    )

    st.pyplot(grapher(x, y, df, graph, hue, out_path))

    with st.form("graphing"):
        save_graph = st.checkbox("Save graph as it is now")
        save_table = st.checkbox("Save dataframe with separated id and sessions", value=True)

        if not st.form_submit_button():
            st.stop()

    if save_graph:
        grapher(x, y, df, graph, hue, out_path, save=True)
    if save_table:
        try:
            h.save_dataset(df, f"{out_path}/entropies_plus", extension='xls')
        except PermissionError as p_error:
            st.error("Can't save the dataset, is `entropies_plus.xls` open somewhere?")
            st.stop()
    st.success("Saved!")
