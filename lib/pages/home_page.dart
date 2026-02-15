import 'package:flutter/material.dart';
import 'package:flutter_blue_plus/flutter_blue_plus.dart';
import 'package:permission_handler/permission_handler.dart';

class HomePage extends StatefulWidget {
  @override
  _HomePageState createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  BluetoothDevice? connectedDevice;
  String selectedMod = '';
  TextEditingController textController = TextEditingController();
  bool hasPermission = false;

  @override
  void initState() {
    super.initState();
    checkPermissions();
  }

  void checkPermissions() async {
    PermissionStatus status = await Permission.bluetoothConnect.request();
    if (!status.isGranted) {
      showDialog(
        context: context,
        builder: (_) => AlertDialog(
          title: Text('Bluetooth permission'),
          content: Text('App does not have Bluetooth permission!'),
          actions: [
            TextButton(
              onPressed: () {
                openAppSettings();
                Navigator.pop(context);
              },
              child: Text('OK'),
            ),
          ],
        ),
      );
    } else {
      setState(() => hasPermission = true);
    }
  }

  bool get isConnected => connectedDevice != null && hasPermission;

  void sendMod(String mod) {
    if (isConnected) {
      print('Sending mod: $mod');
      setState(() => selectedMod = mod);
    }
  }

  void sendText() {
    if (isConnected) {
      String text = textController.text;
      print('Sending text: $text');
      textController.clear();
    }
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: EdgeInsets.all(20),
      child: Column(
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceAround,
            children: ['mod1', 'mod2', 'mod3'].map((mod) {
              return ElevatedButton(
                onPressed: isConnected ? () => sendMod(mod) : null,
                style: ElevatedButton.styleFrom(
                  backgroundColor: selectedMod == mod ? Colors.green : null,
                ),
                child: Text(mod.toUpperCase()),
              );
            }).toList(),
          ),
          SizedBox(height: 30),
          TextField(
            controller: textController,
            enabled: isConnected,
            decoration: InputDecoration(
              border: OutlineInputBorder(),
              labelText: 'Search / Send Text',
            ),
          ),
          SizedBox(height: 10),
          ElevatedButton(
            onPressed: isConnected ? sendText : null,
            child: Text('Send'),
          ),
        ],
      ),
    );
  }
}
