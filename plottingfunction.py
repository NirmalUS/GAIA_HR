import matplotlib.pyplot as plt

def plot_hr(df, property_name = "bp_rp", cmap="coolwarm"):


    fig, ax = plt.subplots(figsize=())
    scatter = ax.scatter(
        df["bp_rp"],
        df["mag"],
        c=df[property_name],
        cmap=cmap,
        s=2
    )
    ax.set_xlabel = ("bp-rp")
    ax.set_ylabel = ("mag")
    ax.set_title = (property_name)
    plt.colorbar(scatter)
    plt.show()

  