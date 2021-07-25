import streamlit as st
import pandas as pd


def format_options(option: str) -> str:
    """
    Formats options for presentation in streamlit
    """
    return option.title()


def grapher(x, y, data, graph, color, save=False):
    """
    Uses seaborn to create the requested graph
    """
    import seaborn as sns
    import matplotlib.pyplot as plt

    graph = graph.strip("plot").strip()
    if ("bar" in graph) | ("box" in graph):
        g = sns.catplot(x=x, y=y, data=data, kind=graph, hue=color)
        plt.xticks(rotation=45, horizontalalignment="right")

    if "scatter" in graph:
        g = sns.relplot(x=x, y=y, data=data, kind=graph, hue=color)

    plt.title(f"{format_options(x)} vs {format_options(y)}")
    plt.xlabel(format_options(x))
    plt.ylabel(format_options(y))

    if save:
        g.savefig(f"output/{graph}_{x}_v_{y}.png", dpi=300)
    return g


def read_entropy_df(filename: str) -> pd.DataFrame:
    """
    Reads in excel file, splits ID column in ID and session
    """
    df = pd.read_excel(f"output/{filename}")
    tag = df["ID"].str.split("_", expand=True)
    tag.columns = ["participant", "session"]
    df = pd.concat([df, tag], axis=1).rename({"ID": "id_sess"}, axis=1)
    part_info = ["participant", "session", "id_sess"]
    df = df[
        part_info + [col for col in df.columns if col not in part_info]
    ]  # reorganize
    return df


def app(filename: str):
    """
    Helps create some simple graphs using the entropies.xls file created by the MatLab script.
    """
    from helpers import helper_functions as h

    df = read_entropy_df(filename)
    st.write(df)

    st.write("## Graphing")
    graph_options = ["bar plot", "box plot", "scatterplot", "facet grid"]
    colx, coly = st.beta_columns(2)
    with colx:
        x = st.selectbox("X axis", options=df.columns, format_func=format_options)
    with coly:
        y = st.selectbox(
            "Y axis", options=df.columns, index=13, format_func=format_options
        )

    color = st.checkbox("Color by session")
    if color:
        hue = "session"
    else:
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

    st.pyplot(grapher(x, y, df, graph, hue))

    with st.form("graphing"):
        save_graph = st.checkbox("Save graph as it is now")
        save_table = st.checkbox("Save dataframe with separated id and sessions")

        if not st.form_submit_button():
            st.stop()

    try:
        if save_graph:
            grapher(x, y, df, graph, hue, save=True)
        if save_table:
            h.save_dataset(df, "output/entropies_id_separated")

        st.success("Saved!")
    except:
        st.error("Something happened, did not save")
        st.stop()
