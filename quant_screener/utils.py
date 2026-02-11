from difflib import get_close_matches

def find_best_match(team_name, valid_teams):
    """
    Fuzzy matches a team name against a list of valid team names.
    Returns the best match if it's confident enough, otherwise returns None.
    """
    # Normalize input (lowercase, strip whitespace)
    team_name = team_name.lower().strip()
    
    # Create a mapping of lowercase -> original names
    valid_map = {t.lower(): t for t in valid_teams}
    
    # Check for exact match first
    if team_name in valid_map:
        return valid_map[team_name]
    
    # Fuzzy match (looking for 60% similarity or better)
    matches = get_close_matches(team_name, valid_map.keys(), n=1, cutoff=0.6)
    
    if matches:
        return valid_map[matches[0]]
        
    return None