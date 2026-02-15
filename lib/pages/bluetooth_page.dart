import 'package:flutter/material.dart';
import 'package:flutter_blue_plus/flutter_blue_plus.dart';
import 'package:permission_handler/permission_handler.dart';

class BluetoothPage extends StatefulWidget {
  @override
  _BluetoothPageState createState() => _BluetoothPageState();
}

class _BluetoothPageState extends State<BluetoothPage> {
  List<ScanResult> scanResults = [];
  bool isScanning = false;

  @override
  void initState() {
    super.initState();
    requestPermissions();
  }

  // Traženje Bluetooth permisija
  void requestPermissions() async {
    await Permission.bluetoothScan.request();
    await Permission.bluetoothConnect.request();
    await Permission.locationWhenInUse.request(); // Za Android < 12
  }

  // Start BLE scan
  void startScan() async {
    setState(() => isScanning = true);
    scanResults.clear();

    // Pokreni scan sa timeout-om od 4 sekunde
    await FlutterBluePlus.startScan(timeout: Duration(seconds: 4));

    // Stream rezultata
    FlutterBluePlus.scanResults.listen((results) {
      setState(() {
        scanResults = results;
      });
    });

    // Nakon što startScan završi, skeniranje više nije aktivno
    setState(() => isScanning = false);
  }

  // Povezivanje na uređaj
  void connectToDevice(BluetoothDevice device) async {
    try {
      await device.connect(timeout: Duration(seconds: 5));

      showDialog(
        context: context,
        builder: (_) => AlertDialog(
          title: Text('Connected'),
          content: Text('Povezivanje sa ${device.name} uspelo!'),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(context),
              child: Text('OK'),
            ),
          ],
        ),
      );
    } catch (e) {
      print('Connection failed: $e');
      showDialog(
        context: context,
        builder: (_) => AlertDialog(
          title: Text('Connection Failed'),
          content: Text('Neuspelo povezivanje sa ${device.name}'),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(context),
              child: Text('OK'),
            ),
          ],
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: EdgeInsets.all(16),
      child: Column(
        children: [
          ElevatedButton(
            onPressed: isScanning ? null : startScan,
            child: Text(isScanning ? 'Scanning...' : 'Start Scan'),
          ),
          SizedBox(height: 16),
          Expanded(
            child: scanResults.isEmpty
                ? Center(child: Text('No devices found'))
                : ListView.builder(
              itemCount: scanResults.length,
              itemBuilder: (context, index) {
                final device = scanResults[index].device;
                return ListTile(
                  title: Text(device.name.isNotEmpty
                      ? device.name
                      : device.id.toString()),
                  subtitle: Text(device.id.toString()),
                  onTap: () => connectToDevice(device),
                );
              },
            ),
          ),
        ],
      ),
    );
  }
}
