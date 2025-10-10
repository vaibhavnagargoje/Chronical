# District Introduction Suggest Edit Feature Documentation

## Overview
This feature allows users to suggest edits to district introduction pages, similar to the chapter suggest edit functionality.

## Files Modified/Created

### 1. Model: `editor/models.py`
Created the `IntroductionEdit` model with the following features:
- **References District model** from `home.models.District`
- **Stores user information**: name, email, user (if authenticated)
- **Section choices**: Introduction Text, Quick Facts, Images, Other
- **Edit types**: correction, addition, clarification, update, other
- **Status tracking**: pending, approved, rejected, in_review
- **File upload support**: Supporting files can be attached
- **Notification option**: Users can opt-in to be notified when reviewed
- **Review tracking**: Reviewed by, review notes, timestamps

### 2. Template: `editor/templates/editor/suggest_intro.html`
Created a complete form template with:
- Breadcrumb navigation
- Section selector (Introduction, Quick Facts, Images, Other)
- Edit type selector
- Text fields for current text, suggested text, and reason
- Sources field
- File upload area
- User information fields (name and email)
- Notification checkbox
- Cancel and submit buttons
- User-friendly styling matching the site theme

### 3. View: `editor/views.py`
Added `suggest_intro_view` function:
- Accepts both GET and POST requests
- Handles form submission
- Saves suggestion to database
- Handles file uploads
- Shows success message
- Redirects back to district detail page

### 4. URL: `editor/urls.py`
Added new URL pattern:
```python
path('district/<int:district_id>/suggest-intro/', views.suggest_intro_view, name='suggest_intro')
```

### 5. District Detail Template: `home/templates/home/district_detail.html`
Updated all "Suggest Edit" buttons to link to the new view:
```django
{% url 'editor:suggest_intro' district.id %}
```
- Desktop version
- Medium screen version
- Mobile version

### 6. Admin: `editor/admin.py`
Registered `IntroductionEdit` model with:
- List display showing key information
- Filters for status, edit type, section, district
- Search functionality
- Organized fieldsets for better UX
- Readonly fields for timestamps

## How It Works

### User Flow:
1. User visits a district detail page
2. Clicks "Suggest Edit" button
3. Fills out the form with:
   - Which section they want to edit
   - Type of edit (correction, addition, etc.)
   - Current text (optional)
   - Suggested text
   - Reason for edit
   - Sources (optional)
   - Supporting files (optional)
   - Their name and email
4. Submits the form
5. Sees success message
6. Redirected back to district page

### Admin Flow:
1. Admin logs into Django admin
2. Goes to "Introduction Edit Suggestions"
3. Can see all suggestions with filters
4. Can review, approve, or reject suggestions
5. Can add review notes
6. Can mark reviewed by and review date

## Database Schema

### IntroductionEdit Model Fields:
- `name` (CharField): Submitter's name
- `email` (EmailField): Submitter's email
- `user` (ForeignKey to User): Link to user if authenticated
- `district` (ForeignKey to District): Which district this edit is for
- `section` (CharField): Which section (introduction, quick_facts, images, other)
- `edit_type` (CharField): Type of edit
- `current_text` (TextField): Current text being edited
- `suggested_text` (TextField): Suggested replacement text
- `reason` (TextField): Reason for the edit
- `sources` (TextField): Supporting sources
- `supporting_file` (FileField): Uploaded supporting file
- `notify_on_review` (BooleanField): Email notification preference
- `status` (CharField): pending, approved, rejected, in_review
- `created_at` (DateTimeField): When submitted
- `updated_at` (DateTimeField): Last updated
- `reviewed_by` (ForeignKey to User): Who reviewed it
- `review_notes` (TextField): Admin notes

## Next Steps (To Do)

1. **Run Migrations**:
   ```bash
   python manage.py makemigrations editor
   python manage.py migrate
   ```

2. **Test the Feature**:
   - Visit a district page
   - Click "Suggest Edit"
   - Fill out and submit the form
   - Check admin panel for submission

3. **Optional Enhancements**:
   - Add email notifications when suggestions are reviewed
   - Create a dashboard for reviewers
   - Add statistics tracking
   - Implement bulk approval/rejection

## URL Pattern
```
/editor/district/<district_id>/suggest-intro/
```

Example:
```
/editor/district/123/suggest-intro/
```

## Permissions
- **Submit Suggestion**: Any user (authenticated or anonymous)
- **View Submissions**: Admin users only
- **Review Suggestions**: Admin users only

## Related Models
- `home.District`: The district being edited
- `auth.User`: For user tracking
- `editor.SuggestEdit`: Similar model for chapter edits
