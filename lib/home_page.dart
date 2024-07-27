// lib/home_page.dart
import 'package:flutter/material.dart';
import 'sign_page.dart';
import 'voice_page.dart';

class HomePage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Keystroke'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            ElevatedButton(
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => SignPage()),
                );
              },
              child: Text('Sign'),
            ),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => VoicePage()),
                );
              },
              child: Text('Voice'),
            ),
          ],
        ),
      ),
    );
  }
}