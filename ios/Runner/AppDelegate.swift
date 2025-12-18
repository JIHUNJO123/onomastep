import Flutter
import UIKit
import AppTrackingTransparency
import GoogleMobileAds

@main
@objc class AppDelegate: FlutterAppDelegate {
  override func application(
    _ application: UIApplication,
    didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?
  ) -> Bool {
    GeneratedPluginRegistrant.register(with: self)
    
    // Request ATT authorization after a short delay
    if #available(iOS 14, *) {
      DispatchQueue.main.asyncAfter(deadline: .now() + 1.0) {
        ATTrackingManager.requestTrackingAuthorization { status in
          // Initialize Google Mobile Ads after ATT response
          GADMobileAds.sharedInstance().start(completionHandler: nil)
        }
      }
    } else {
      GADMobileAds.sharedInstance().start(completionHandler: nil)
    }
    
    return super.application(application, didFinishLaunchingWithOptions: launchOptions)
  }
}
