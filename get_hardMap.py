import re

def parse_transition_map(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # Split by "Event:"
    raw_events = re.split(r'\n-+\n', text.strip())
    transition_map = {}

    for section in raw_events:
        event_match = re.search(r'Event:\s*(.+)', section)
        if not event_match:
            continue
        event_name = event_match.group(1).strip()

        follows_section = re.search(r'Followed by:\n((?:\s{4}.+\n)+)', section)
        not_follows_section = re.search(r'Not followed by:\n((?:\s{4}.+\n)+)', section)
        percentage_match = re.search(r'Percentage_of_appearance:\s*([\d.]+)%', section)

        follows_by = {}
        if follows_section:
            for line in follows_section.group(1).strip().splitlines():
                match = re.match(r'\s*(.+?):\s*([\d.]+)%', line)
                if match:
                    follows_by[match.group(1).strip()] = float(match.group(2))

        not_follows_by = []
        if not_follows_section:
            for line in not_follows_section.group(1).strip().splitlines():
                nf = line.strip()
                if nf:
                    not_follows_by.append(nf)

        percentage = float(percentage_match.group(1)) if percentage_match else 0.0

        transition_map[event_name] = {
            "followed_by": follows_by,
            "not_followed_by": not_follows_by,
            "percentage_of_appearance": percentage
        }

    return transition_map

if __name__ == "__main__":
    file_path = "TCP/TCP_0_500_BiasedSATPAT_hard_map.txt"
    hard_map = parse_transition_map(file_path)
    for event, data in hard_map.items():
        print(f"Event: {event}")

        print("  Followed by:")
        for follower, percent in data.get('followed_by', {}).items():
            print(f"    {follower}: {percent}%")

        print("  Not followed by:")
        for non_follower in data.get('not_followed_by', []):
            print(f"    {non_follower}")

        print(f"Percentage_of_appearance: {hard_map[event]['percentage_of_appearance']}%")
        print("-" * 30)
