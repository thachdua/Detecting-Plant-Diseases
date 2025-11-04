import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:geolocator/geolocator.dart';
import 'package:geocoding/geocoding.dart';
import 'package:google_maps_flutter/google_maps_flutter.dart';
import 'package:ai_detection/core/theme/app_theme.dart';
import 'package:ai_detection/core/widgets/modern_button.dart';

class LocationPickerDialog extends StatefulWidget {
  final String? initialLocation;

  const LocationPickerDialog({super.key, this.initialLocation});

  @override
  State<LocationPickerDialog> createState() => _LocationPickerDialogState();
}

class _LocationPickerDialogState extends State<LocationPickerDialog> {
  final TextEditingController _locationController = TextEditingController();
  final TextEditingController _searchController = TextEditingController();
  GoogleMapController? _mapController;
  LatLng _selectedLocation = const LatLng(10.8231, 106.6297);
  String? _address;
  bool _isLoading = false;
  final _mapKey = GlobalKey();

  @override
  void initState() {
    super.initState();
    _locationController.text = widget.initialLocation ?? '';
    _initializeLocation();
  }

  @override
  void dispose() {
    _locationController.dispose();
    _searchController.dispose();
    _mapController?.dispose();
    super.dispose();
  }

  Future<void> _initializeLocation() async {
    setState(() => _isLoading = true);
    if (widget.initialLocation != null && widget.initialLocation!.isNotEmpty) {
      try {
        final locations = await locationFromAddress(widget.initialLocation!);
        if (locations.isNotEmpty) {
          final newLocation = LatLng(locations.first.latitude, locations.first.longitude);
          setState(() {
            _selectedLocation = newLocation;
            _isLoading = false;
          });
          await Future.delayed(const Duration(milliseconds: 500));
          await _mapController?.animateCamera(
            CameraUpdate.newLatLngZoom(newLocation, 15),
          );
          await _updateAddressFromLocation();
        } else {
          setState(() => _isLoading = false);
        }
      } catch (_) {
        setState(() => _isLoading = false);
      }
    } else {
      await _getCurrentLocation();
    }
  }

  Future<void> _getCurrentLocation() async {
    setState(() => _isLoading = true);
    try {
      bool serviceEnabled = await Geolocator.isLocationServiceEnabled();
      if (!serviceEnabled) {
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text(
                'Location services are disabled',
                style: GoogleFonts.inter(),
              ),
              backgroundColor: AppTheme.errorRed,
            ),
          );
        }
        setState(() => _isLoading = false);
        return;
      }

      LocationPermission permission = await Geolocator.checkPermission();
      if (permission == LocationPermission.denied) {
        permission = await Geolocator.requestPermission();
        if (permission == LocationPermission.denied) {
          if (mounted) {
            ScaffoldMessenger.of(context).showSnackBar(
              SnackBar(
                content: Text(
                  'Location permissions are denied',
                  style: GoogleFonts.inter(),
                ),
                backgroundColor: AppTheme.errorRed,
              ),
            );
          }
          setState(() => _isLoading = false);
          return;
        }
      }

      if (permission == LocationPermission.deniedForever) {
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text(
                'Location permissions are permanently denied',
                style: GoogleFonts.inter(),
              ),
              backgroundColor: AppTheme.errorRed,
            ),
          );
        }
        setState(() => _isLoading = false);
        return;
      }

      final position = await Geolocator.getCurrentPosition();
      final newLocation = LatLng(position.latitude, position.longitude);
      setState(() {
        _selectedLocation = newLocation;
      });
      await _mapController?.animateCamera(
        CameraUpdate.newLatLngZoom(newLocation, 15),
      );
      await _updateAddressFromLocation();
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(
              'Error getting location: $e',
              style: GoogleFonts.inter(),
            ),
            backgroundColor: AppTheme.errorRed,
          ),
        );
      }
    }
    setState(() => _isLoading = false);
  }

  Future<void> _updateAddressFromLocation() async {
    try {
      final placemarks = await placemarkFromCoordinates(
        _selectedLocation.latitude,
        _selectedLocation.longitude,
      );
      if (placemarks.isNotEmpty) {
        final place = placemarks.first;
        final address = '${place.street ?? ''}, ${place.locality ?? ''}, ${place.country ?? ''}'
            .replaceAll(RegExp(r'^,\s*|,\s*$'), '');
        setState(() {
          _address = address;
          _locationController.text = address;
        });
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(
              'Error getting address: $e',
              style: GoogleFonts.inter(),
            ),
            backgroundColor: AppTheme.errorRed,
          ),
        );
      }
    }
  }

  Future<void> _searchLocation() async {
    if (_searchController.text.isEmpty) return;
    setState(() => _isLoading = true);
    try {
      final locations = await locationFromAddress(_searchController.text);
      if (locations.isNotEmpty) {
        setState(() {
          _selectedLocation = LatLng(locations.first.latitude, locations.first.longitude);
        });
        await _mapController?.animateCamera(
          CameraUpdate.newLatLng(_selectedLocation),
        );
        await _updateAddressFromLocation();
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(
              'Location not found: $e',
              style: GoogleFonts.inter(),
            ),
            backgroundColor: AppTheme.errorRed,
          ),
        );
      }
    }
    setState(() => _isLoading = false);
  }

  void _onMapTap(LatLng location) {
    setState(() {
      _selectedLocation = location;
    });
    _mapController?.animateCamera(
      CameraUpdate.newLatLngZoom(location, 15),
    );
    _updateAddressFromLocation();
  }

  @override
  Widget build(BuildContext context) {
    return Dialog(
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(24),
      ),
      child: ConstrainedBox(
        constraints: BoxConstraints(
          maxHeight: MediaQuery.of(context).size.height * 0.85,
        ),
        child: Container(
          padding: const EdgeInsets.all(24),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              Row(
                children: [
                  Container(
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: AppTheme.accentBlue,
                      borderRadius: BorderRadius.circular(16),
                    ),
                    child: Icon(
                      Icons.location_on_rounded,
                      color: AppTheme.primaryGreen,
                      size: 24,
                    ),
                  ),
                  const SizedBox(width: 16),
                  Expanded(
                    child: Text(
                      'Select Location',
                      style: GoogleFonts.inter(
                        fontSize: 24,
                        fontWeight: FontWeight.w700,
                        color: AppTheme.textPrimary,
                      ),
                    ),
                  ),
                  IconButton(
                    icon: const Icon(Icons.close),
                    onPressed: () => Navigator.pop(context),
                  ),
                ],
              ),
              const SizedBox(height: 24),
              TextFormField(
                controller: _searchController,
                decoration: InputDecoration(
                  labelText: 'Search location',
                  prefixIcon: const Icon(Icons.search_outlined),
                  suffixIcon: IconButton(
                    icon: _isLoading
                        ? const SizedBox(
                            width: 20,
                            height: 20,
                            child: CircularProgressIndicator(strokeWidth: 2),
                          )
                        : const Icon(Icons.search),
                    onPressed: _searchLocation,
                  ),
                  labelStyle: GoogleFonts.inter(),
                ),
                style: GoogleFonts.inter(),
                onFieldSubmitted: (_) => _searchLocation(),
              ),
              const SizedBox(height: 16),
              TextFormField(
                controller: _locationController,
                decoration: InputDecoration(
                  labelText: 'Selected Location',
                  prefixIcon: const Icon(Icons.location_on_outlined),
                  labelStyle: GoogleFonts.inter(),
                ),
                style: GoogleFonts.inter(),
                readOnly: true,
              ),
              const SizedBox(height: 16),
              Row(
                children: [
                  Expanded(
                    child: OutlinedButton.icon(
                      onPressed: _isLoading ? null : _getCurrentLocation,
                      icon: const Icon(Icons.my_location),
                      label: Text(
                        'My Location',
                        style: GoogleFonts.inter(fontWeight: FontWeight.w600),
                      ),
                      style: OutlinedButton.styleFrom(
                        padding: const EdgeInsets.symmetric(vertical: 12),
                      ),
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 24),
              Row(
                children: [
                  Expanded(
                    child: OutlinedButton(
                      onPressed: () => Navigator.pop(context),
                      style: OutlinedButton.styleFrom(
                        padding: const EdgeInsets.symmetric(vertical: 16),
                      ),
                      child: Text(
                        'Cancel',
                        style: GoogleFonts.inter(fontWeight: FontWeight.w600),
                        maxLines: 1,
                        overflow: TextOverflow.ellipsis,
                      ),
                    ),
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    flex: 2,
                    child: ModernButton(
                      label: 'Confirm',
                      icon: Icons.check_circle_outline,
                      onPressed: _locationController.text.isEmpty
                          ? null
                          : () {
                              Navigator.pop(context, _locationController.text);
                            },
                      isLoading: _isLoading,
                    ),
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }
}
