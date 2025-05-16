"""Discord Reaction Messages
Send messages using discord reactions
"""

from time import sleep
from os.path import exists

from requests import put, get


def text_to_id(text: str, alphabet: dict, duplicate_alphabet: dict) -> list:
    """Convert text to a list of discord emoji IDs.

    Args:
        text (str): The text to convert
        alphabet (dict): Mapping of letters to emoji IDs
        duplicate_alphabet (dict): Mapping of letters to secondary emoji IDs for duplicates letters

    Returns:
        list: List of emoji IDs or None if too many duplicated letters
    """
    used_letters = set()
    duplcated_letters = set()
    result = []

    for char in text.upper():
        if char == " ":
            continue

        if char not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            continue

        if char in duplcated_letters:
            return None

        if char in used_letters:
            result.append(duplicate_alphabet[char])
            duplcated_letters.add(char)
        else:
            result.append(alphabet[char])
            used_letters.add(char)

    return result


def add_reactions(
    emoji_ids: list, message: str, token: str, channel_id: str, message_id: str
) -> bool:
    """Add reactions to a message.

    Args:
        emoji_ids (list): List of emoji IDs to add as reactions
        message (str): Original message text
        token (str): Discord authorization token
        channel_id (str): Discord channel ID
        message_id (str): Discord message ID

    Returns:
        bool: True if all reactions were successfully added, False otherwise
    """
    headers = {"accept": "*/*", "authorization": token}

    for i, emoji_id in enumerate(emoji_ids):
        url = (
            f"https://discord.com/api/v9/channels/{channel_id}"
            f"/messages/{message_id}/reactions/{emoji_id}/@me"
        )
        response = put(url, headers=headers, timeout=10)

        if response.status_code == 204:
            print(f"Successfully sent reaction for '{message[i].upper()}'")
        elif response.status_code == 429:
            try:
                retry_after = response.json().get("retry_after", 1)
                print(f"Rate limited. Waiting {retry_after}s before retrying...")
                sleep(retry_after)
                response = put(url, headers=headers, timeout=10)
                if response.status_code == 204:
                    print(
                        f"Successfully sent reaction for '{message[i].upper()}' after rate limit"
                    )
                else:
                    print(
                        f"Failed to add reaction for '{message[i].upper()}' after rate limit."
                        f"Status: {response.status_code}"
                    )
                    return False
            except (ValueError, KeyError) as err:
                print(f"Error handling rate limit: {err}")
                return False
        else:
            print(
                f"Failed to add reaction for '{message[i].upper()}'."
                f"Status: {response.status_code}"
            )
            return False

        sleep(1)

    return True


def fetch_message_ids(
    token: str, channel_id: str, limit: int, starting_id: str
) -> list:
    """Fetch message IDs from a Discord channel.

    Args:
        token (str): Discord authorization token
        channel_id (str): Discord channel ID
        limit (int): Maximum number of messages to fetch
        starting_id (str): ID of the message to start from

    Returns:
        list: List of message IDs
    """
    headers = {"accept": "*/*", "authorization": token}
    params = {"limit": limit, "after": starting_id}
    url = f"https://discord.com/api/v9/channels/{channel_id}/messages"

    response = get(url, headers=headers, params=params, timeout=10)

    if response.status_code != 200:
        print(f"Failed to fetch messages. Status: {response.status_code}")
        return []

    messages = response.json()
    ids = [msg["id"] for msg in messages]
    ids.append(starting_id)

    ids.reverse()

    return ids


def get_infos() -> tuple:
    """Get user input for token, channel ID, and message ID.

    Returns:
        tuple: (token, channel_id, message_id)
    """
    with open("token.txt", encoding="utf-8") as file:
        token = file.read().strip()

    if not token:
        token = input("Enter your discord token: ")

    channel_id = input("Enter the channel ID: ")
    message_id = input(
        "Enter the starting message ID: "
    )
    return token, channel_id, message_id


def main(token: str, channel_id: str, message_id: str) -> None:
    """Main function.

    Args:
        token (str): Discord authorization token
        channel_id (str): Discord channel ID
        message_id (str): Discord message ID
    """
    assert exists("emoji_ids.txt"), "Warning: emoji_ids.txt not found."

    emoji_ids = []
    with open("emoji_ids.txt", encoding="utf-8") as file:
        emoji_ids = [line.strip() for line in file]

    assert (
        len(emoji_ids) >= 26
    ), f"emoji_ids.txt doesn't contain enough ids: {len(emoji_ids)}/26"
    assert len(emoji_ids) <= 26, f"emoji_ids.txt have too many ids: {len(emoji_ids)}/26"

    message = input("Enter your message: ")
    words = message.split()

    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    alphabet = {
        l: f"%F0%9F%87%{hex(0xA6 + i)[2:].upper()}" for i, l in enumerate(letters)
    }
    duplicate_alphabet = {
        l: f"regional_indicator_{l.lower()}~1%3A{emoji_ids[i]}"
        for i, l in enumerate(letters)
    }

    for i, word in enumerate(words):
        text_ids = text_to_id(word, alphabet, duplicate_alphabet)
        if text_ids is None:
            word = input(
                f"Word '{word}' has too many duplicated letters.\nPlease retry. "
            )
            main(token, channel_id, message_id)
            return

    message_ids = fetch_message_ids(token, channel_id, len(words) - 1, message_id)
    if len(words) > len(message_ids):
        print(
            f"Not enough messages ({len(message_ids)}) to react to all words ({len(words)})"
            "Please retry."
        )
        main(token, channel_id, message_id)
        return

    for i, word in enumerate(words):
        text_ids = text_to_id(word, alphabet, duplicate_alphabet)
        sent = add_reactions(text_ids, word, token, channel_id, message_ids[i])

        if not sent:
            print(f"Failed to add reactions for word '{word}'. Stopping.")
            break

        print(f"Successfully added reactions for word '{word}'")
        if not i == len(words) - 1:
            sleep(2)

    print("Finished adding reactions to all messages")


if __name__ == "__main__":
    TOKEN, CHANNEL_ID, MESSAGE_ID = get_infos()
    main(TOKEN, CHANNEL_ID, MESSAGE_ID)
