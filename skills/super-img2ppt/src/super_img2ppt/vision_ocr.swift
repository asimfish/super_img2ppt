import Foundation
import ImageIO
import Vision

struct Line: Codable {
    let text: String
    let confidence: Float
    let box: [Double]
}

do {
    guard CommandLine.arguments.count >= 2 else {
        throw NSError(domain: "super-img2ppt", code: 1, userInfo: [NSLocalizedDescriptionKey: "An image path is required"])
    }
    let url = URL(fileURLWithPath: CommandLine.arguments[1])
    guard let source = CGImageSourceCreateWithURL(url as CFURL, nil),
          let image = CGImageSourceCreateImageAtIndex(source, 0, nil) else {
        throw NSError(domain: "super-img2ppt", code: 2, userInfo: [NSLocalizedDescriptionKey: "Image cannot be decoded"])
    }
    let request = VNRecognizeTextRequest()
    request.recognitionLevel = .accurate
    request.usesLanguageCorrection = false
    request.recognitionLanguages = CommandLine.arguments.count >= 3 ? CommandLine.arguments[2].components(separatedBy: ",") : ["zh-Hans", "en-US"]
    try VNImageRequestHandler(cgImage: image).perform([request])
    let lines: [Line] = (request.results ?? []).compactMap { observation in
        guard let candidate = observation.topCandidates(1).first else { return nil }
        let b = observation.boundingBox
        return Line(text: candidate.string, confidence: candidate.confidence,
                    box: [b.minX * Double(image.width), (1 - b.maxY) * Double(image.height), b.width * Double(image.width), b.height * Double(image.height)])
    }
    let data = try JSONEncoder().encode(lines)
    FileHandle.standardOutput.write(data)
} catch {
    FileHandle.standardError.write(Data(error.localizedDescription.utf8))
    exit(1)
}
