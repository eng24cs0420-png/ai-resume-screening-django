import re


def extract_candidate_info(text):

    # -----------------------------------------
    # EMAIL
    # -----------------------------------------

    email_match = re.search(
        r'[\w\.-]+@[\w\.-]+\.\w+',
        text
    )

    if email_match:

        email = email_match.group(0)

    else:

        email = "Not detected"


    # -----------------------------------------
    # PHONE
    # -----------------------------------------

    phone_match = re.search(
        r'(\+91[\s-]?)?[6-9]\d{9}',
        text
    )

    if phone_match:

        phone = phone_match.group(0)

    else:

        phone = "Not detected"


    # -----------------------------------------
    # NAME
    # -----------------------------------------

    lines = [

        line.strip()

        for line in text.splitlines()

        if line.strip()

    ]


    name = "Not detected"


    if lines:

        # Look through first few lines
        # to find a likely candidate name

        for line in lines[:5]:

            # Ignore lines containing
            # email/phone/web addresses

            if "@" in line:
                continue

            if "http" in line.lower():
                continue

            if re.search(
                r'\d{7,}',
                line
            ):
                continue


            # Name normally has
            # 1-5 words

            words = line.split()


            if 1 <= len(words) <= 5:

                name = line

                break


    return {

        "name": name,

        "email": email,

        "phone": phone,

    }