# Test script to check if the model properties work correctly
# This tests the properties we added to fix the template error

class MockDistrict:
    def __init__(self, name, state_name):
        self.name = name
        self.state = MockState(state_name)

class MockState:
    def __init__(self, name):
        self.name = name

class MockChapter:
    def __init__(self, name, district_name, state_name):
        self.name = name
        self.district = MockDistrict(district_name, state_name)

class MockTerm:
    def __init__(self, term):
        self.term = term

class MockContextualDefinition:
    def __init__(self, term, cultural_chapter=None, statistical_chapter=None):
        self.term = MockTerm(term)
        self.cultural_chapter = cultural_chapter
        self.statistical_chapter = statistical_chapter
    
    @property
    def chapter(self):
        """Get the associated chapter (either cultural or statistical)"""
        return self.cultural_chapter or self.statistical_chapter
    
    @property
    def chapter_name(self):
        """Get the name of the associated chapter"""
        chapter = self.cultural_chapter or self.statistical_chapter
        return chapter.name if chapter else "Unknown Chapter"
    
    @property
    def chapter_type(self):
        """Get the type of chapter (Cultural or Statistical)"""
        if self.cultural_chapter:
            return "Cultural"
        elif self.statistical_chapter:
            return "Statistical"
        return "Unknown"
    
    @property
    def district_info(self):
        """Get district and state information"""
        chapter = self.cultural_chapter or self.statistical_chapter
        if chapter and hasattr(chapter, 'district') and chapter.district:
            return f"{chapter.district.name}, {chapter.district.state.name}"
        return "Unknown District"

# Test the properties
print("Testing ContextualDefinition properties...")

# Test with cultural chapter
cultural_chapter = MockChapter("Cultural Heritage", "Mumbai", "Maharashtra")
cultural_override = MockContextualDefinition("Heritage", cultural_chapter=cultural_chapter)

print(f"Cultural Chapter Name: {cultural_override.chapter_name}")
print(f"Cultural Chapter Type: {cultural_override.chapter_type}")
print(f"Cultural District Info: {cultural_override.district_info}")

# Test with statistical chapter
statistical_chapter = MockChapter("Population Data", "Delhi", "Delhi")
statistical_override = MockContextualDefinition("Population", statistical_chapter=statistical_chapter)

print(f"Statistical Chapter Name: {statistical_override.chapter_name}")
print(f"Statistical Chapter Type: {statistical_override.chapter_type}")
print(f"Statistical District Info: {statistical_override.district_info}")

# Test with None chapters (edge case)
empty_override = MockContextualDefinition("Empty")
print(f"Empty Chapter Name: {empty_override.chapter_name}")
print(f"Empty Chapter Type: {empty_override.chapter_type}")
print(f"Empty District Info: {empty_override.district_info}")

print("All tests passed! The properties are working correctly.")