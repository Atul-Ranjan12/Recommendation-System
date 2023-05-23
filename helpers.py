PATH = "./images_256_256"


# Function to get the image path
def get_image_path(article):
    dir_name = "0" + str(article)[:2]
    file_name = "0" + str(article) + ".jpg"
    image_path = PATH + "/" + dir_name + "/" + file_name
    return image_path


def get_article_attributes(id, df):
    """
    Gets necessary attributes of the articles
    :param id: article_id
    :param df: article dataframe
    :return: dictionary of all attributes
    """
    info = dict()
    info["article_id"] = id
    df = df.loc[df["article_id"] == id]
    info["name"] = str(list(df["perceived_colour_value_name"])[0]) + " " + str(list(df["prod_name"])[0])
    info["section"] = str(list(df["section_name"])[0])
    info["description"] = str(list(df["detail_desc"])[0])
    info["attributes"] = str(list(df["product_type_name"])[0])
    info["image_path"] = get_image_path(id)

    return info



