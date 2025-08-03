//
//  GCTIntegration.swift
//  Extension for Apple Intelligence Chat to integrate with GCT Assistant
//
//  This file should be added to the Apple Intelligence Chat Xcode project
//

import Foundation
import SwiftUI

// MARK: - GCT Data Models

struct GCTProfile: Codable {
    let userId: String
    let staticCoherence: Double
    let variables: GCTVariables
    let timestamp: String
}

struct GCTVariables: Codable {
    let psi: Double  // Internal Consistency
    let rho: Double  // Wisdom Integration
    let q: Double    // Moral Activation
    let f: Double    // Social Belonging
}

struct GCTResponse: Codable {
    let success: Bool
    let response: String
    let type: String
    let data: [String: Any]?
    
    enum CodingKeys: String, CodingKey {
        case success, response, type, data
    }
    
    init(from decoder: Decoder) throws {
        let container = try decoder.container(keyedBy: CodingKeys.self)
        success = try container.decode(Bool.self, forKey: .success)
        response = try container.decode(String.self, forKey: .response)
        type = try container.decode(String.self, forKey: .type)
        data = try container.decodeIfPresent([String: Any].self, forKey: .data)
    }
}

// MARK: - GCT Integration Manager

@MainActor
class GCTIntegrationManager: ObservableObject {
    static let shared = GCTIntegrationManager()
    
    @Published var isConnected = false
    @Published var currentProfile: GCTProfile?
    @Published var lastError: String?
    
    private let baseURL = "http://localhost:5001"
    private let session = URLSession.shared
    
    // MARK: - Query Detection
    
    /// Check if a message should be processed by GCT
    func shouldProcessWithGCT(_ message: String) -> Bool {
        let gctKeywords = [
            "coherence", "wellness", "balance", "gct",
            "internal consistency", "wisdom", "moral activation", "belonging",
            "recovery plan", "temporal pattern", "group dynamics"
        ]
        
        let lowercased = message.lowercased()
        return gctKeywords.contains { lowercased.contains($0) }
    }
    
    /// Process a query through GCT
    func processGCTQuery(_ query: String, userId: String = "apple_user") async -> GCTResponse? {
        guard let url = URL(string: "\(baseURL)/api/apple-intelligence/query") else {
            lastError = "Invalid URL"
            return nil
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        let body = ["query": query, "user_id": userId]
        
        do {
            request.httpBody = try JSONSerialization.data(withJSONObject: body)
            
            let (data, response) = try await session.data(for: request)
            
            guard let httpResponse = response as? HTTPURLResponse,
                  httpResponse.statusCode == 200 else {
                lastError = "Server error"
                return nil
            }
            
            let gctResponse = try JSONDecoder().decode(GCTResponse.self, from: data)
            return gctResponse
            
        } catch {
            lastError = error.localizedDescription
            return nil
        }
    }
    
    /// Get the current user's coherence profile
    func getCoherenceProfile(userId: String = "apple_user") async -> GCTProfile? {
        guard let url = URL(string: "\(baseURL)/api/profile/\(userId)") else {
            return nil
        }
        
        do {
            let (data, _) = try await session.data(from: url)
            let response = try JSONDecoder().decode([String: GCTProfile].self, from: data)
            currentProfile = response["profile"]
            return currentProfile
        } catch {
            lastError = error.localizedDescription
            return nil
        }
    }
    
    /// Submit a quick coherence assessment
    func submitQuickAssessment(userId: String = "apple_user",
                              consistency: Double,
                              wisdom: Double,
                              energy: Double,
                              belonging: Double) async -> Bool {
        guard let url = URL(string: "\(baseURL)/api/assessment/tier1") else {
            return false
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        let body: [String: Any] = [
            "user_id": userId,
            "responses": [
                "consistency": consistency,
                "wisdom": wisdom,
                "energy": energy,
                "belonging": belonging
            ],
            "age": 30  // Default age
        ]
        
        do {
            request.httpBody = try JSONSerialization.data(withJSONObject: body)
            let (_, response) = try await session.data(for: request)
            
            guard let httpResponse = response as? HTTPURLResponse,
                  httpResponse.statusCode == 200 else {
                return false
            }
            
            return true
        } catch {
            lastError = error.localizedDescription
            return false
        }
    }
    
    /// Check backend connectivity
    func checkConnection() async {
        guard let url = URL(string: "\(baseURL)/health") else {
            isConnected = false
            return
        }
        
        do {
            let (_, response) = try await session.data(from: url)
            
            if let httpResponse = response as? HTTPURLResponse,
               httpResponse.statusCode == 200 {
                isConnected = true
            } else {
                isConnected = false
            }
        } catch {
            isConnected = false
            lastError = error.localizedDescription
        }
    }
}

// MARK: - GCT-Enhanced Language Model Session

extension LanguageModelSession {
    /// Create a GCT-enhanced session with system instructions
    static func createGCTEnhancedSession() -> LanguageModelSession {
        let gctInstructions = """
        You are an AI assistant integrated with the Grounded Coherence Theory (GCT) system.
        
        When users ask about their coherence, wellness, balance, or personal development:
        1. First, mention that you can check their GCT coherence profile
        2. Explain the four variables in simple terms:
           - Ψ (Psi): Internal Consistency - alignment of thoughts, feelings, and actions
           - ρ (Rho): Wisdom Integration - learning from experience
           - q: Moral Activation - acting on values
           - f: Social Belonging - quality of connections
        3. Provide actionable insights based on their profile
        4. Suggest specific improvements for their lowest variables
        
        When you detect coherence-related queries, prefix your response with:
        [GCT_ANALYSIS] for coherence checks
        [GCT_RECOVERY] for improvement plans
        [GCT_PATTERN] for temporal patterns
        
        Always be supportive, encouraging, and focused on practical improvements.
        """
        
        return LanguageModelSession(instructions: gctInstructions)
    }
}

// MARK: - GCT UI Components

struct GCTCoherenceView: View {
    let profile: GCTProfile
    
    var body: some View {
        VStack(alignment: .leading, spacing: 16) {
            // Overall Coherence
            HStack {
                Text("Overall Coherence")
                    .font(.headline)
                Spacer()
                Text(String(format: "%.2f/4.0", profile.staticCoherence))
                    .font(.title2)
                    .foregroundColor(coherenceColor)
            }
            
            Divider()
            
            // Variables
            VStack(spacing: 12) {
                VariableRow(
                    symbol: "Ψ",
                    name: "Internal Consistency",
                    value: profile.variables.psi
                )
                VariableRow(
                    symbol: "ρ",
                    name: "Wisdom Integration",
                    value: profile.variables.rho
                )
                VariableRow(
                    symbol: "q",
                    name: "Moral Activation",
                    value: profile.variables.q
                )
                VariableRow(
                    symbol: "f",
                    name: "Social Belonging",
                    value: profile.variables.f
                )
            }
        }
        .padding()
        .glassEffect(.regular)
    }
    
    var coherenceColor: Color {
        switch profile.staticCoherence {
        case 0..<1.5: return .red
        case 1.5..<2.5: return .orange
        case 2.5..<3.5: return .green
        default: return .blue
        }
    }
}

struct VariableRow: View {
    let symbol: String
    let name: String
    let value: Double
    
    var body: some View {
        HStack {
            Text(symbol)
                .font(.system(size: 20, weight: .bold, design: .serif))
                .frame(width: 30)
            
            Text(name)
                .font(.subheadline)
            
            Spacer()
            
            // Progress bar
            GeometryReader { geometry in
                ZStack(alignment: .leading) {
                    RoundedRectangle(cornerRadius: 4)
                        .fill(Color.gray.opacity(0.2))
                        .frame(height: 8)
                    
                    RoundedRectangle(cornerRadius: 4)
                        .fill(valueColor)
                        .frame(width: geometry.size.width * value, height: 8)
                }
            }
            .frame(width: 100, height: 8)
            
            Text(String(format: "%.2f", value))
                .font(.caption)
                .foregroundColor(.secondary)
                .frame(width: 35, alignment: .trailing)
        }
    }
    
    var valueColor: Color {
        switch value {
        case 0..<0.4: return .red
        case 0.4..<0.6: return .orange
        case 0.6..<0.8: return .green
        default: return .blue
        }
    }
}

// MARK: - Integration with ContentView

extension ContentView {
    /// Process message with GCT integration
    func processWithGCT(_ message: String) async -> String? {
        let gctManager = GCTIntegrationManager.shared
        
        if gctManager.shouldProcessWithGCT(message) {
            if let response = await gctManager.processGCTQuery(message) {
                return response.response
            }
        }
        
        return nil
    }
}