from hash_table import HashTable

# AI has been used to write some of the code for this script, but it has been reviewed and modified by me to ensure accuracy and clarity.

def test_basic_insert_search():
    """Inserted keys should be retrievable, with the correct values."""
    ht = HashTable(m=8)
    ht.insert("apple", 3)
    ht.insert("banana", 5)
    assert ht.search("apple") == 3
    assert ht.search("banana") == 5
    print("test_basic_insert_search passed.")


def test_update_existing_key():
    """Inserting an existing key should update its value, not duplicate it."""
    ht = HashTable(m=8)
    ht.insert("apple", 3)
    ht.insert("apple", 7)
    assert ht.search("apple") == 7
    assert ht.n == 1, f"expected n=1 after update, got {ht.n}"
    print("test_update_existing_key passed.")


def test_delete():
    """Deleting a key should remove it and update the count."""
    ht = HashTable(m=8)
    ht.insert("apple", 3)
    ht.insert("banana", 5)
    ht.delete("apple")
    assert ht.n == 1
    try:
        ht.search("apple")
        assert False, "expected KeyError after deleting 'apple'"
    except KeyError:
        pass
    print("test_delete passed.")


def test_missing_key_raises():
    """Searching or deleting a key that was never inserted should raise KeyError."""
    ht = HashTable(m=8)
    for op in (lambda: ht.search("ghost"), lambda: ht.delete("ghost")):
        try:
            op()
            assert False, "expected KeyError for missing key"
        except KeyError:
            pass
    print("test_missing_key_raises passed.")


def test_collision_handling():
    """Force every key into the same slot and confirm chaining still works."""
    ht = HashTable(m=1)          # m=1 guarantees every key collides
    ht.insert("a", 1)
    ht.insert("b", 2)
    ht.insert("c", 3)
    assert ht.search("a") == 1
    assert ht.search("b") == 2
    assert ht.search("c") == 3
    ht.delete("b")
    assert ht.n == 2
    try:
        ht.search("b")
        assert False, "expected KeyError after deleting 'b'"
    except KeyError:
        pass
    print("test_collision_handling passed.")



if __name__ == "__main__":
    test_basic_insert_search()
    test_update_existing_key()
    test_delete()
    test_missing_key_raises()
    test_collision_handling()
    print("\nAll hash table tests passed.")