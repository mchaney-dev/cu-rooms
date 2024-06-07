def parse_rooms(data) -> list:
    entries = []

    for i in range(0, len(data)):
        entry = {
            'item_id': None,
            'abbrev': None,
            'building': None,
            'room': None,
            'categories': [],
            'features': [],
            'layouts': None,
            'capacity': None,
            'max_capacity': None,
            'events': None
        }

        entry.update({'item_id': data[i]['row'][0].get('itemId')})
        entry.update({'abbrev': data[i]['row'][0].get('itemName').split(' ')[0]})
        entry.update({'building': data[i]['row'][1].split(' ', 1)[1]})
        entry.update({'room': data[i]['row'][1].split(' ', 1)[0]})
        entry.update({'categories': list(data[i]['row'][2].split(', '))})
        entry.update({'features': list(data[i]['row'][3].split(', '))})
        entry.update({'layouts': list(data[i]['row'][4].split(', '))})
        entry.update({'capacity': data[i]['row'][5]})
        entry.update({'max_capacity': data[i]['row'][6]})
        entries.append(entry)
    return entries

def parse_events(data) -> list:
    entries = []

    for i in range(0, len(data)):
        if data[i].get('rsrv') is None:
            break
        for j in range(0, len(data[i].get('rsrv'))):
            locations = []
            entry = {
                'event_id': None,
                'start': None,
                'end': None,
                'name': None,
                'locations': None,
                'all_day': None
            }
            entry.update({'event_id': data[i].get('rsrv')[j].get('event_id')})
            entry.update({'start': data[i].get('rsrv')[j].get('rsrv_start_dt')})
            entry.update({'end': data[i].get('rsrv')[j].get('rsrv_end_dt')})
            entry.update({'name': data[i].get('rsrv')[j].get('event_name')})
            entry.update({'all_day': bool(data[i].get('rsrv')[j].get('all_day'))})
            for k in range(0, len(data[i].get('rsrv')[j].get('subject'))):
                locations.append(data[i].get('rsrv')[j].get('subject')[k].get('itemName'))
            entry.update({'locations': locations})
            entries.append(entry)
    return entries