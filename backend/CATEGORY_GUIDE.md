# Quick Reference: Modifying Categories

## Location
File: `backend/utils/categorizer.py`

## Current Categories

```python
CATEGORY_KEYWORDS = {
    'Academic': [...],
    'Music': [...],
    'Sports': [...],
    'Arts': [...],
    'Cultural': [...],
    'Social': [...],
    'Recreation': [...],
    'Greek Life': [...],
    'Other': (default)
}
```

## Common Tasks

### ✅ Add a Keyword to Existing Category

```python
# In categorizer.py
'Sports': [
    'sports', 'soccer', 'basketball', 'football', ...,
    'pickleball',  # ← Add this line
]
```

### ✅ Create a New Category

```python
CATEGORY_KEYWORDS = {
    # ...existing...
    'Gaming': [
        'gaming', 'esports', 'video games', 'competitive gaming',
        'game development', 'board games', 'rpg', 'dnd'
    ]
}
```

Then rebuild the database:
```bash
flask clear-db
flask init-db
flask seed-db
```

### ✅ Remove a Category

```python
# Option 1: Delete the key (clubs will categorize to 'Other')
del CATEGORY_KEYWORDS['Greek Life']

# Option 2: Keep it but don't use it (can add back later)
# Just comment out or leave as-is
```

### ✅ Test Your Changes

```bash
cd backend
python3
```

```python
from app import app
from utils.categorizer import ClubCategorizer

# Get updated category list
categories = ClubCategorizer.get_category_list()
print(categories)

# Test a specific club
category = ClubCategorizer.categorize(
    "Gaming Club",
    "Compete in video games and esports tournaments"
)
print(f"Gaming Club → {category}")
```

## How Categorization Works

1. **Combine** club name + description into one text
2. **Count** matches for each category's keywords (case-insensitive)
3. **Select** category with highest match count
4. **Default** to 'Other' if no category matches

## Example Keyword Lists

### 🎓 Academic
```
coding, programming, computer, science, engineering, math,
physics, chemistry, biology, business, economics, research,
debate, case competition, consulting, entrepreneurship, startup
```

### 🎵 Music
```
music, band, orchestra, jazz, choir, singing, instrument,
performance, musician, acoustic, electric, vocal, symphony
```

### ⚽ Sports
```
sports, soccer, basketball, football, tennis, baseball,
volleyball, lacrosse, crew, rowing, swimming, rugby,
frisbee, ultimate, athletic, fitness, yoga, martial arts
```

### 🎨 Arts
```
art, drawing, painting, sculpture, design, photography,
film, theater, drama, dance, visual, creative, animation
```

## Pro Tips

- **Be specific**: Add single words, not phrases (easier to match)
- **Cover variants**: Add both singular/plural forms if needed
  ```python
  'Music': [..., 'musician', 'musicians', ...]
  ```
- **Test first**: Always test categorization before re-seeding database
- **Check overlaps**: Keywords shouldn't be too generic (e.g., avoid "club", "student")

## Reverting Changes

If you break something, just restore the backup:

```bash
# See original version in git
git show HEAD:backend/utils/categorizer.py

# Restore if needed
git checkout backend/utils/categorizer.py
```

---

**Last Updated**: November 18, 2025
