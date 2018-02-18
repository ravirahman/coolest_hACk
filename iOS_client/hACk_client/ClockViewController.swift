//
//  ViewController.swift
//  HGCircularSlider
//
//  Created by Suyash Saxena on 02/18/2018.
//  Copyright (c) 2018 Suyash Saxena. All rights reserved.
//

import UIKit
import HGCircularSlider
import Alamofire
import Foundation
import SwiftyJSON

class ClockViewController: UIViewController {
    
    var lo = 65.0 as CGFloat
    var hi = 75.0 as CGFloat

    @IBOutlet weak var durationLabel: UILabel!
    @IBOutlet weak var bedtimeLabel: UILabel!
    @IBOutlet weak var wakeLabel: UILabel!
    @IBOutlet weak var rangeCircularSlider: RangeCircularSlider!
    @IBOutlet weak var button: UIButton!
    @IBOutlet weak var cost: UILabel!
    @IBOutlet weak var energy: UILabel!
    @IBOutlet weak var hack: UILabel!
    @IBOutlet weak var topBar: UIView!
    @IBOutlet weak var midBar: UIView!
    @IBOutlet weak var bottomBar: UIView!
    @IBOutlet weak var thermoButton: UIButton!
    @IBOutlet weak var acImage: UIImageView!
    @IBOutlet weak var expected: UILabel!
    @IBOutlet weak var final: UILabel!
    
    var speed: Int = 0
    
    var curr: Float = 75.0
    
    weak var timer: Timer?
    
    weak var timerAC: Timer?

    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        button.backgroundColor = .clear
        button.layer.cornerRadius = 5
        button.layer.borderWidth = 1
        button.layer.borderColor = UIColor.white.cgColor
        
        thermoButton.backgroundColor = .clear
        thermoButton.layer.cornerRadius = 5
        thermoButton.layer.borderWidth = 1
        thermoButton.layer.borderColor = UIColor.white.cgColor
        
        
        // setup O'clock
        rangeCircularSlider.startThumbImage = UIImage(named: "ice")
        rangeCircularSlider.endThumbImage = UIImage(named: "fire")
        
        let dayInSeconds = 24 * 60 * 60
        rangeCircularSlider.maximumValue = CGFloat(dayInSeconds)
        rangeCircularSlider.startPointValue = 79200
        rangeCircularSlider.endPointValue = 7200
    
        startAC()
        updateTexts(rangeCircularSlider)
        
    }
    
    func stuff(s: Int){
        let headers = ["content-type": "application/json"]
        let parameters = ["speed": s] as [String : Any]
        
        print("**SPEED**: \(s)")
        
        let postData = try? JSONSerialization.data(withJSONObject: parameters, options: [])
        guard let data = postData else {
            return
        }
        
        let request = NSMutableURLRequest(url: NSURL(string: "http://25412fc2.ngrok.io/setAC")! as URL,
                                          cachePolicy: .useProtocolCachePolicy,
                                          timeoutInterval: 10.0)
        request.httpMethod = "POST"
        request.allHTTPHeaderFields = headers
        request.httpBody = data as Data
        
        let session = URLSession.shared
        let dataTask = session.dataTask(with: request as URLRequest, completionHandler: { (data, response, error) -> Void in
            if (error != nil) {
                print(error)
            } else {
                let httpResponse = response as? HTTPURLResponse
            }
        })
        
        dataTask.resume()
    }
    

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    @IBAction func buttonTap(_ sender: Any) {
        // python
        let url = URL(string: "http://40.71.34.70:5000/temp")!
        
        let params: [String: Float] = ["alpha": 0.009,
                                       "beta": 0.2,
                                       "current": curr,
                                       "min": Float(lo+10),
                                       "max": Float(hi+70)]
        
        Alamofire.request(url, method: .post, parameters: params, encoding: URLEncoding.default, headers: nil).validate(statusCode: 200..<600).responseJSON { response in
            
            switch response.result {
            case .success:
                if let value = response.result.value as? [String: Any]{
                    
                    let c = value["cost_perc"]! as! Float
                    let e = value["en_perc"]! as! Float
                    let temp = value["response"]! as! Float
                    let exp = value["expected"]! as! Float
                    
                    self.cost.text = NSString(format: "%.2f", c) as String
                    self.cost.text = self.cost.text! + "%"
                    self.energy.text = NSString(format: "%.2f", e) as String
                    self.energy.text = self.energy.text! + "%"
                    self.hack.text = NSString(format: "%.1f", temp) as String
                    self.final.text = NSString(format: "%.1f", exp) as String
                    self.startTimer(lo: exp)
                }
                
            case .failure(let error):
                print("RESPONSE ERROR: \(error)")
                
            }
            
        }
    }
    
    func startAC(){
        timerAC?.invalidate()
        timerAC = Timer.scheduledTimer(withTimeInterval: 5, repeats: true) { [weak self] _ in
            self?.fetchColor()
        }
    }
    
    func startTimer(lo: Float) {
        timer?.invalidate()   // just in case you had existing `Timer`, `invalidate` it before we lose our reference to it
        if (curr > lo){
            timer = Timer.scheduledTimer(withTimeInterval: 4, repeats: true) { [weak self] _ in
                if (lo >= (self?.curr)! - 0.1){
                    self?.stopTimer()
                    self?.acImage.alpha = 0.0
                }
                else {
                    self?.curr = (self?.curr)! - 0.1
                    self?.expected.text = NSString(format: "%.1f", (self?.curr)!) as String
                    
                    if ((self?.curr)! - lo > 12){
                        self?.speed = 240
                    }
                    else if ((self?.curr)! - lo > 8){
                        self?.speed = 160
                    }
                    else if ((self?.curr)! - lo > 4){
                        self?.speed = 80
                    }
                }
            }
        }
        else if (curr < lo){
            timer = Timer.scheduledTimer(withTimeInterval: 5.0, repeats: true) { [weak self] _ in
                if (lo < (self?.curr)!){
                    self?.stopTimer()
                }
                else {
                    self?.curr = (self?.curr)! + 0.1
                    self?.expected.text = NSString(format: "%.1f", (self?.curr)!) as String
                }
            }
        }
    }
    
    func stopTimer() {
        timer?.invalidate()
    }
    
    // if appropriate, make sure to stop your timer in `deinit`
    
    deinit {
        stopTimer()
    }
    
    
    func fetchColor(){
        //node
        let url = URL(string: "http://25412fc2.ngrok.io/thermo")!
        
        Alamofire.request(url, method: .get, encoding: URLEncoding.default, headers: nil).validate(statusCode: 200..<600).responseJSON { response in
            
            switch response.result {
            case .success:
                if let value = response.result.value as? [String: Any]{
                    
                    let fan = value["fan"]! as! Int
                    let sigTop = value["sigTop"]! as! Float
                    let sigMid = value["sigMid"]! as! Float
                    let sigBottom = value["sigBottom"]! as! Float
                    
                    print("FAN:\(fan)")
                    if (fan == 1){
                        UIView.animate(withDuration: 1.5, animations: {
                            self.acImage.alpha = 1.0
                            
                        })
                        self.stuff(s: 240)
                    }
                    else {
                        UIView.animate(withDuration: 1.5, animations: {
                            self.acImage.alpha = 0.0
                        })
                        self.stuff(s: 0)
                    }
                    
                    UIView.animate(withDuration: 1.5, animations: {
                        self.topBar.alpha = CGFloat(sigTop)
                        self.midBar.alpha = CGFloat(sigMid)
                        self.bottomBar.alpha = CGFloat(sigBottom)
                    })
                }
                
            case .failure(let error):
                print("RESPONSE ERROR: \(error)")
                
            }
        }
    }
    
    @IBAction func onColorTap(_ sender: Any) {
        fetchColor()
    }
    
    
    @IBAction func updateTexts(_ sender: AnyObject) {
        
        adjustValue(value: &rangeCircularSlider.startPointValue)
        adjustValue(value: &rangeCircularSlider.endPointValue)

        
        lo = rangeCircularSlider.startPointValue/2880*2
        print("Lo: \(lo+10)");
        
        if ((lo+10) > 70)
        {
            bedtimeLabel.text = NSString(format: "%.0f °F", lo+70) as String
        }
        else {
            bedtimeLabel.text = NSString(format: "%.0f °F", lo+10) as String
        }

        
        hi = rangeCircularSlider.endPointValue/2880*2
        print("Hi: \(hi+70)");
        
        if ((hi + 70) < 0)
        {
            wakeLabel.text = NSString(format: "%.0f °F", lo-60) as String
        }
        else {
            wakeLabel.text = NSString(format: "%.0f °F", hi+70) as String
        }
    }
    
    func adjustValue(value: inout CGFloat) {
        let minutes = value / 60
        let adjustedMinutes =  ceil(minutes / 5.0) * 5
        value = adjustedMinutes * 60
    }

}

