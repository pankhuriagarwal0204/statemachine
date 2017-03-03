morcha_state_map = {
    0: 'secure',
    1: 'intrusion_detected',
    2: 'intrusion_verified',
    3: 'marked_safe',
    4: 'sos_raised'
}

morcha_states = []

for state in morcha_state_map.iteritems():
    v = state[1]
    morcha_states.append(v)

morcha_transitions = [
    # secure --> detected
    {'trigger': 'intrusion_detected', 'source': morcha_state_map[0], 'dest': morcha_state_map[1],
     'after': 'after_intrusion_detected'},
    # detected --> detected : increase attempts
    {'trigger': 'intrusion_detected', 'source': morcha_state_map[1], 'dest': morcha_state_map[1],
     'after': 'increase_attempts'},
    # detected --> secure : non human
    {'trigger': 'area_secure_button_pressed', 'source': morcha_state_map[1], 'dest': morcha_state_map[0],
     'after': 'intrusion_never_happened'},
    # detected --> verified
    {'trigger': 'intrusion_verified_button_pressed', 'source': morcha_state_map[1], 'dest': morcha_state_map[2],
     'after': 'after_intrusion_verified'},
    # verified --> marked safe
    {'trigger': 'area_secure_button_pressed', 'source': morcha_state_map[2], 'dest': morcha_state_map[3],
     'after': 'after_marked_safe'},
    # verified --> verified : detected(increase attempts)
    {'trigger': 'intrusion_detected', 'source': morcha_state_map[2], 'dest': morcha_state_map[2],
     'after': 'increase_attempts'},
    # verified --> sos raised
    {'trigger': 'sos_raised_button_pressed', 'source': morcha_state_map[2], 'dest': morcha_state_map[4],
     'after': 'after_sos_raised'},
    # marked safe --> detected : to be done
    {'trigger': 'intrusion_detected', 'source': morcha_state_map[3], 'dest': morcha_state_map[1],
     'after': 'increase_attempts'},  ## to be done
    # marked safe --> verified : to be done
    {'trigger': 'intrusion_verified_button_pressed', 'source': morcha_state_map[3], 'dest': morcha_state_map[2],
     'after': 'marked_safe_to_verified'},  ## to be done,
    # marked safe --> security confirmed
    {'trigger': 'security_confirmed_event', 'source': morcha_state_map[3], 'dest': morcha_state_map[0],
     'after': 'after_security_confirmed'},
    # sos raised --> marked safe
    {'trigger': 'area_secure_button_pressed', 'source': morcha_state_map[4], 'dest': morcha_state_map[3],
     'after': 'after_marked_safe'},
    # sos raised --> security confirmed
    {'trigger': 'security_confirmed_event', 'source': morcha_state_map[4], 'dest': morcha_state_map[0],
     'after': 'after_security_confirmed'},

]


