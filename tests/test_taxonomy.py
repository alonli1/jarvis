from jarvis.taxonomy import classify_tags, expanded_tags

TAXONOMY = {
    "gravitational_eft": {"all": ["gravity", "eft"]},
    "inverse_uv_reconstruction": {"phrases": ["inverse eft matching"]},
}


def test_controlled_tags_match_topic_rules_and_manuscript_phrases():
    assert classify_tags(["gravity", "eft"], TAXONOMY) == ["gravitational_eft"]
    assert classify_tags([], TAXONOMY, "An inverse EFT matching pipeline") == [
        "inverse_uv_reconstruction"
    ]


def test_expanded_tags_keep_normalized_source_topics():
    assert expanded_tags(["Quantum Gravity", "EFT"], TAXONOMY) == [
        "quantum_gravity",
        "eft",
    ]
