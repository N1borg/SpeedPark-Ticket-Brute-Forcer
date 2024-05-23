# -*- coding: utf-8 -*-

def display_loading_bar(start: int, end: int, current: int, width:int = 50) -> None:
    total = end - start
    if total <= 0:
        print("Invalid range. Start should be less than end.")
        return

    if not (start <= current <= end):
        print("Current value out of range.")
        return

    percent = (current - start) / total
    bar = ('#' * int(width * percent)).ljust(width)
    percentage_str = f'{int(percent * 100)}%'
    spaces = ' ' * (4 - len(percentage_str))
    print(f'\r[{bar}] {spaces}{percentage_str} ({current}/{end})', end='', flush=True)
