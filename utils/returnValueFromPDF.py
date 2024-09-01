
def returnValueFromPDF(key: str, pdf: str) -> str:
    text_target = key

    text_target_index = pdf.find(text_target)

    text_target_index_end = (
        text_target_index
        # + 2
        + pdf[text_target_index: len(pdf)].find("\n")
    )

    # result = pdf[text_target_index:text_target_index_end].replace(
    #     text_target, "").replace(",", ".")
    result = pdf[text_target_index:text_target_index_end].replace(
        text_target, "")

    return result


def returnValueFromPDFPositions(key_start: str, key_end: str, pdf: str) -> str:
    text_target = key_start

    text_target_index = pdf.find(text_target)

    text_target_index_end = (
        text_target_index
        # + 2
        + pdf[text_target_index: len(pdf)].find(key_end)
    )

    # result = pdf[text_target_index:text_target_index_end].replace(
    #     text_target, "").replace(",", ".")
    result = pdf[text_target_index:text_target_index_end].replace(
        text_target, "")

    return result
