morcha_state_map = {
    'secure': 'secure',
    'intrusion_detected': 'intrusion_detected',
    'intrusion_verified': 'intrusion_verified',
    'marked_safe': 'marked_safe',
    'sos_raised': 'sos_raised'
}

morcha_states = morcha_state_map.keys()

morcha_transitions = [
    # secure --> detected
    {'trigger': 'intrusion_detected_event', 'source': morcha_state_map['secure'], 'dest': morcha_state_map['intrusion_detected'],
     'after': 'after_intrusion_detected'},
    # secure --> verified
    {'trigger': 'intrusion_verified_button_pressed', 'source': morcha_state_map['secure'], 'dest': morcha_state_map['intrusion_verified'],
     'after': 'after_intrusion_detected_to_verified'},
    # detected --> detected : increase attempts
    {'trigger': 'intrusion_detected_event', 'source': morcha_state_map['intrusion_detected'], 'dest': morcha_state_map['intrusion_detected'],
     'after': 'increase_attempts'},
    # detected --> secure : non human
    {'trigger': 'area_secure_button_pressed', 'source': morcha_state_map['intrusion_detected'], 'dest': morcha_state_map['secure'],
     'after': 'intrusion_never_happened'},
    # detected --> verified
    {'trigger': 'intrusion_verified_button_pressed', 'source': morcha_state_map['intrusion_detected'], 'dest': morcha_state_map['intrusion_verified'],
     'after': 'after_intrusion_verified'},
    # verified --> marked safe
    {'trigger': 'area_secure_button_pressed', 'source': morcha_state_map['intrusion_verified'], 'dest': morcha_state_map['marked_safe'],
     'after': 'after_marked_safe'},
    # verified --> verified : detected(increase attempts)
    {'trigger': 'intrusion_detected_event', 'source': morcha_state_map['intrusion_verified'], 'dest': morcha_state_map['intrusion_verified'],
     'after': 'increase_attempts'},
    # verified --> sos raised
    {'trigger': 'sos_raised_button_pressed', 'source': morcha_state_map['intrusion_verified'], 'dest': morcha_state_map['sos_raised'],
     'after': 'after_sos_raised'},
    # marked safe --> detected : to be done
    {'trigger': 'intrusion_detected_event', 'source': morcha_state_map['marked_safe'], 'dest': morcha_state_map['intrusion_detected'],
     'after': 'marked_safe_to_detected'},  ## to be done
    # marked safe --> verified : to be done
    {'trigger': 'intrusion_verified_button_pressed', 'source': morcha_state_map['marked_safe'], 'dest': morcha_state_map['intrusion_verified'],
     'after': 'marked_safe_to_verified'},  ## to be done,
    # marked safe --> security confirmed
    {'trigger': 'security_confirmed_event', 'source': morcha_state_map['marked_safe'], 'dest': morcha_state_map['secure'],
     'after': 'after_security_confirmed'},
    # sos raised --> marked safe
    {'trigger': 'area_secure_button_pressed', 'source': morcha_state_map['sos_raised'], 'dest': morcha_state_map['marked_safe'],
     'after': 'after_marked_safe'},
    # sos raised --> security confirmed
    {'trigger': 'security_confirmed_event', 'source': morcha_state_map['sos_raised'], 'dest': morcha_state_map['secure'],
     'after': 'after_security_confirmed'},
]