import 'package:flutter/material.dart';
import 'package:flutter_blue_plus/flutter_blue_plus.dart';

class BottomNavBar extends StatefulWidget {
  final int currentIndex;
  final Function(int) onTabSelected;

  const BottomNavBar({
    required this.currentIndex,
    required this.onTabSelected,
  });

  @override
  _BottomNavBarState createState() => _BottomNavBarState();
}

class _BottomNavBarState extends State<BottomNavBar> {
  bool isBluetoothOn = false;

  @override
  void initState() {
    super.initState();
    // Prati stanje Bluetooth adaptera
    FlutterBluePlus.adapterState.listen((state) {
      setState(() {
        isBluetoothOn = state == BluetoothAdapterState.on;
      });
    });
  }

  @override
  Widget build(BuildContext context) {
    return BottomNavigationBar(
      currentIndex: widget.currentIndex,
      onTap: widget.onTabSelected,
      items: [
        BottomNavigationBarItem(
          icon: Icon(Icons.home),
          label: 'Home',
        ),
        BottomNavigationBarItem(
          icon: Icon(
            isBluetoothOn ? Icons.bluetooth_connected : Icons.bluetooth_disabled,
          ),
          label: 'Bluetooth',
        ),
      ],
    );
  }
}
