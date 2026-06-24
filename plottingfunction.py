import matplotlib.pyplot as plt

def plot_hr(df, property_name, label, cmap="coolwarm"):

    fig, ax = plt.subplots(figsize=(8, 10))

    scatter = ax.scatter(
        df["bp_rp"],
        df["mag"],
        c=df[property_name],
        cmap=cmap,
        s=2
    )
    plt.style.use(["dark_background"])

    ax.invert_yaxis()

    ax.set_xlabel("BP - RP")
    ax.set_ylabel("Absolute Magnitude")

    ax.set_title(
        f"HR Diagram Colored by {label}"
    )


    cbar = plt.colorbar(scatter)

    cbar.set_label(label)

    plt.show()