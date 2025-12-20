import re

# Read the N2 file
file_path = r'C:\Users\hooni\Desktop\jlpt_vocab_app_n2\lib\screens\word_list_screen.dart'

with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Fix 1: Change _restoreScrollPosition to use item index instead of pixel offset
old_restore = '''  Future<void> _restoreScrollPosition() async {
    if (widget.isFlashcardMode) return;
    final prefs = await SharedPreferences.getInstance();
    final offset = prefs.getDouble(_scrollOffsetKey) ?? 0.0;
    if (offset > 0 && _listScrollController.hasClients) {
      _listScrollController.jumpTo(offset);
    } else if (offset > 0) {
      // Controller not attached yet, wait for it
      WidgetsBinding.instance.addPostFrameCallback((_) {
        if (_listScrollController.hasClients && mounted) {
          _listScrollController.jumpTo(offset);
        }
      });
    }
  }'''

new_restore = '''  Future<void> _restoreScrollPosition() async {
    if (widget.isFlashcardMode) return;
    final prefs = await SharedPreferences.getInstance();
    final position = prefs.getInt(_positionKey) ?? 0;
    if (position > 0) {
      // Wait for the ListView to be built
      WidgetsBinding.instance.addPostFrameCallback((_) {
        if (_listScrollController.hasClients && mounted) {
          // Each item is approximately 80 pixels
          _listScrollController.jumpTo(position * 80.0);
        }
      });
    }
  }'''

content = content.replace(old_restore, new_restore)

# Fix 2: Change _saveScrollPosition to save item index instead of pixel offset
old_save = '''  Future<void> _saveScrollPosition(double offset) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setDouble(_scrollOffsetKey, offset);
  }'''

new_save = '''  Future<void> _saveScrollPosition(double offset) async {
    final prefs = await SharedPreferences.getInstance();
    // Save as item index instead of pixel offset for consistency
    final itemIndex = (offset / 80.0).round();
    await prefs.setInt(_positionKey, itemIndex);
  }'''

content = content.replace(old_save, new_save)

# Write back
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("N2 scroll position fix applied successfully!")
