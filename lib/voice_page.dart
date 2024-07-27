import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart'; // For picking files
import 'package:record/record.dart'; // For recording audio
import 'dart:io'; // For file operations

class VoicePage extends StatefulWidget {
  @override
  _VoicePageState createState() => _VoicePageState();
}

class _VoicePageState extends State<VoicePage> {
  File? _audioFile;
  final Record _record = Record();
  bool _isRecording = false;

  // Function to pick an audio file
  Future<void> _pickAudio() async {
    final picker = ImagePicker();
    final pickedFile = await picker.pickVideo(source: ImageSource.gallery); // Use pickVideo for picking audio

    setState(() {
      if (pickedFile != null) {
        _audioFile = File(pickedFile.path);
      } else {
        print('No audio file selected.');
      }
    });
  }

  // Function to start recording audio
  Future<void> _startRecording() async {
    if (await _record.hasPermission()) {
      await _record.start();
      setState(() {
        _isRecording = true;
      });
    } else {
      print('Permission denied.');
    }
  }

  // Function to stop recording audio
  Future<void> _stopRecording() async {
    final path = await _record.stop();
    setState(() {
      _isRecording = false;
      if (path != null) {
        _audioFile = File(path);
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Voice Page'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            ElevatedButton(
              onPressed: _pickAudio,
              child: Text('Pick Audio File'),
            ),
            ElevatedButton(
              onPressed: _isRecording ? _stopRecording : _startRecording,
              child: Text(_isRecording ? 'Stop Recording' : 'Start Recording'),
            ),
            if (_audioFile != null)
              Text('Audio File Path: ${_audioFile!.path}'),
          ],
        ),
      ),
    );
  }
}