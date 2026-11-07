import 'package:flutter_test/flutter_test.dart';
import 'package:saves/main.dart';

void main() {
  testWidgets('shows the saves.fm placeholder', (tester) async {
    await tester.pumpWidget(const SavesApp());
    expect(find.text('saves.fm'), findsOneWidget);
  });
}
