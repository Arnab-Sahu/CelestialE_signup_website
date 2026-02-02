from argon2 import PasswordHasher
from django.contrib import messages
from django.shortcuts import render
import os
import firebase_admin
from firebase_admin import credentials, firestore
from pathlib import Path


BASE_DIRECTORY = Path(__file__).resolve().parent.parent

JSON_PATH = os.path.join(BASE_DIRECTORY, 'firebase_admin.json')



try:
    # This is the "Public" way: check if the app already exists
    firebase_admin.get_app()
except ValueError:
    # If get_app() fails, it means it's not initialized yet
    cred = credentials.Certificate(JSON_PATH)
    firebase_admin.initialize_app(cred)
db = firestore.client()

# Create your views here.
def index(request):
    faqs = [
        {
            "q":"What is this NFT Marketplace?",
            "a":"Our marketplace is a premium, curated platform built on Polygon's blockchain, offering exclusive digital collectibles vetted for quality and originality.",
        },
        {
            "q": "How is this marketplace different from others?",
            "a": " We focus on curation and exclusivity, ensuring only premium NFTs are listed, combined with fast, eco-friendly transactions powered by Polygon.",
        },
        {
            "q": "When will the marketplace launch?",
            "a": "The marketplace is currently in development. Early signups give you priority access and exclusive previews ahead of the official launch.",
        },
        {
            "q": "How do I signup early?",
            "a": "Click the 'Sign Up' or 'Get Early Access' button and provide your details. Early members receive updates and VIP benefits when we launch.",
        },
        {
            "q": "What is this NFT Marketplace?",
            "a": "Our marketplace is a premium, curated platform built on Polygon's blockchain, offering exclusive digital collectibles vetted for quality and originality.",
        },
        {
            "q": "What are NFTs beyond digital art?",
            "a": "NFTs represent unique digital ownership that can include art, music, access passes, memberships, virtual assets, and much more.",
        },
        {
            "q": "Will I need a crypto wallet?",
            "a": "Yes. To buy, sell, or hold NFTs on our platform, you'll need a compatible wallet that supports Polygon network tokens.",
        },
        {
            "q": "Can I sell my NFTs here?",
            "a": "Yes. Our platform allows creators to mint, list, and sell their NFTs to a global audience within a curated community.",
        },
        {
            "q": "What is this NFT Marketplace?",
            "a": "Our marketplace is a premium, curated platform built on Polygon's blockchain, offering exclusive digital collectibles vetted for quality and originality.",
        },
        {
            "q": "What fees are involved?",
            "a": "Transaction fees are competitively low, leveraging Polygon's scalability. Detailed fee info will be available upon launch.",
        },
        {
            "q": "How can I get support or help?",
            "a": "Our dedicated support team is available via email to assist you before and after the marketplace goes live.",
        },
    ]
    return render(request, "index.html", {"faqs": faqs})

def terms_view(request):
    tnc = [
        {
            "num":"1.",
            "heading":"Early Access Invitation",
            "text":"Your early signup grants you priority access to updates, previews, and invitations ahead of the official marketplace launch. This does not guarantee immediate access to the full platform or any NFTs until the official launch.",
        },
        {
            "num": "2.",
            "heading": "User Eligibility",
            "text": "You confirm that you are at least 18 years old, or of legal age in your jurisdiction, and have the legal capacity to enter into this agreement.",
        },
        {
            "num": "3.",
            "heading": "Information Accuracy",
            "text": "You agree to provide accurate and truthful information during signup and to keep your account information up to date.",
        },
        {
            "num": "4.",
            "heading": "Data Processing and Privacy",
            "text": "By signing up, you consent to the collection, storage, and use of your personal information as described in our Privacy Policy. This includes communication about the marketplace, promotional offers, and updates. You may opt out at any time through communication preferences.",
        },
        {
            "num": "5.",
            "heading": "No Financial Commitment",
            "text": "Early signup is free and does not obligate you to make any purchases or engage in transactions on the platform. Any future purchases will be subject to additional terms and conditions at launch.",
        },
        {
            "num": "6.",
            "heading": "Risks and Disclaimers",
            "text": "As the marketplace is under development, features and services described are subject to change. By signing up early, you acknowledge that services are provided \"as is\" and no warranties are made regarding launch timelines or content availability.",
        },
        {
            "num": "7.",
            "heading": "Communication Consent",
            "text": "You agree to receive occasional emails and announcements related to the marketplace development, launch notifications, and exclusive early access opportunities. You may unsubscribe at any time.",
        },
        {
            "num": "8.",
            "heading": "Intellectual Property",
            "text": "All content shared with early users remains the property of the marketplace and its partners. You agree not to share confidential information or materials until officially released.",
        },
        {
            "num": "9.",
            "heading": "Termination of Early Access",
            "text": "The marketplace reserves the right to terminate or suspend early access privileges at its discretion, including for violations of these terms or inappropriate conduct.",
        },
        {
            "num": "10.",
            "heading": "Governing Law and Dispute Resolution",
            "text": "These terms shall be governed by the laws applicable to the marketplace’s jurisdiction. Any disputes arising from early signup will be resolved through amicable discussions or mediation before legal action.",
        }
    ]
    return render(request, "terms.html", {"terms":tnc})

def signup_view(request):
    if request.method == "POST":
        email = request.POST.get("email").strip().lower()
        username = request.POST.get("username").strip()

        try:
            # Check if username exists
            if db.collection('users').document(email).get().exists:
                messages.warning(request, "This email is already registered.")
                return render(request, "signup.html")

            # Save to Firestore
            db.collection('users').document(email).set({
                'email': email,
                'username': username,
                'created_at': firestore.firestore.SERVER_TIMESTAMP,
            })

            messages.success(request, f"Welcome to the CelestialE, {username}!")
            #return redirect('create_account')

        except Exception as e:
            print(f"Error: {e}")
            messages.error(request, "Celestial connection failed. Check your console.")
            return render(request, "signup.html")

    return render(request, "signup.html")
