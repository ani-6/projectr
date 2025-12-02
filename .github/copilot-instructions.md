# AI Coding Agent Instructions for ProjectR

## Project Overview
ProjectR is a Django 5.2 web application with a modular architecture centered on user authentication and dashboard functionality. The codebase is organized as a Django project (`config/`) with reusable apps (`apps/`).

**Tech Stack:**
- Django 5.2.8
- SQLite3 database (development)
- Class-based views (CBV) and function-based views (FBV)
- Django's built-in authentication system with user groups

---

## Architecture & Key Components

### App Structure
- **`apps/accounts/`**: User authentication, registration, profile management
  - Uses Django's `User` model extended via `OneToOneField` to custom `Profile` model
  - Contains `customLoginView` (extends `LoginView` with "remember me" functionality)
  - Profile fields: gender, headline, bio, profile/cover pictures
  
- **`apps/dashboard/`**: Main application views (currently minimal)
  - Contains the home page view
  
- **`apps/common/`**: Shared utilities (currently empty stubs for `mixins.py`, `helpers.py`, `decorators.py`)
  - Intended location for reusable decorators, mixins, and helper functions

### User Model Extension Pattern
The project extends Django's `User` model via a `Profile` model using `OneToOneField`:
```python
# apps/accounts/models.py
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_profile")
    # ... custom fields
```
Access profile via `request.user.user_profile` throughout the codebase.

### User Groups
New users are automatically assigned to the "Users" group on registration:
```python
# apps/accounts/views.py - registerView.post()
group = Group.objects.get(name='Users')
user.groups.add(group)
```
Ensure "Users" group exists (typically created via data migration or admin).

---

## Critical Developer Workflows

### Running the Development Server
```bash
python manage.py runserver
```

### Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Create Superuser
```bash
python manage.py createsuperuser
```

### Testing
```bash
python manage.py test
```

### Static Files
```bash
python manage.py collectstatic
```
Static files collected to `staticfiles/` directory.

---

## Project Conventions & Patterns

### URL Routing Pattern
- Apps use namespaced URLs (e.g., `'account'`, `'dashboard'`)
- URLs defined in app-level `urls.py` and included in `config/urls.py`:
  ```python
  path('accounts/', include('apps.accounts.urls', namespace='accounts'))
  path('', include('apps.dashboard.urls', namespace='dashboard'))
  ```
- Use `reverse_lazy()` or `redirect()` with `'namespace:name'` format

### Forms Pattern
- All forms in `apps/<app>/forms.py`
- Custom form fields use Bootstrap CSS classes (`class: 'form-control'`)
- Example: `customAuthenticationForm` extends `AuthenticationForm` with "remember me" checkbox
- Forms provide custom error messages and placeholder attributes

### View Pattern - Class-Based Views (Preferred)
- Use Django's `View`, `LoginView`, `PasswordChangeView`, `PasswordResetView` classes
- Example redirect for authenticated users in `registerView.dispatch()`:
  ```python
  if request.user.is_authenticated:
      return redirect(to='/')
  ```

### Session Handling
- "Remember me" feature sets session expiry to 600 seconds if unchecked:
  ```python
  if not remember_me:
      request.session.set_expiry(600)
      request.session.modified = True
  ```

### Media & Profile Pictures
- Default profile picture: `Accounts/profile_images/default.jpg`
- Default cover picture: `Accounts/cover_images/_default.jpg`
- Thumbnails generated via (currently commented) helper functions

### Authentication Methods
- Login supports both **username AND email** authentication (see `customLoginView.post()`)
- Email authentication fallback implemented

---

## File References by Purpose

| Purpose | File |
|---------|------|
| Authentication views | `apps/accounts/views.py` |
| Auth forms | `apps/accounts/forms.py` |
| User/Profile models | `apps/accounts/models.py` |
| Settings & middleware | `config/settings.py` |
| Root URL config | `config/urls.py` |
| Shared utilities | `apps/common/` (empty, ready for expansion) |

---

## Integration Points & Dependencies

- **Django Admin**: Enabled at `/admin/`, site header set to "ProjectR"
- **Authentication Middleware**: Standard Django auth middleware in use
- **Session-based Login**: Standard Django session authentication
- **Media Files**: Configured via `MEDIA_ROOT` and `MEDIA_URL`
- **Email Backend**: Password reset views configured but email backend not explicitly set (uses console in development)

---

## Known Patterns & Code Quirks

1. **TODO: Thumbnail generation** - Helper functions in `apps/accounts/views.py` are commented out. Implement in `apps/common/helpers.py` if needed.
2. **TODO: Media URL** - `MEDIA_URL` is commented out in settings.py
3. **Form naming convention**: Forms use snake_case (`register_form`, `customAuthenticationForm`)
4. **View naming convention**: Views use `camelCase` followed by `View` suffix
5. **Bootstrap integration**: All form fields styled with Bootstrap classes
