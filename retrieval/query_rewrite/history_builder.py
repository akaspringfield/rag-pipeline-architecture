"""
Convert stored chat messages into a prompt-friendly history string.
"""

class HistoryBuilder:

    @staticmethod
    def build(messages):

        if not messages:
            return ""

        lines = []

        for msg in messages:

            lines.append(
                f"{msg.role.capitalize()}: {msg.content}"
            )

        return "\n".join(lines)