#!/usr/bin/env python3
"""
MULTIBET Page Converter - Fixed Version
This will properly convert all pages to match the first template
"""

import os
import re
import glob
from datetime import datetime
import random

# Image pool
IMGUR_IMAGES = [
    "https://i.imgur.com/ygFk5oT.jpg", "https://i.imgur.com/rxC9MAj.jpg",
    "https://i.imgur.com/mG2T8IS.jpg", "https://i.imgur.com/jzFnQlJ.jpg",
    "https://i.imgur.com/w6dLBn6.jpg", "https://i.imgur.com/z5vDEJs.jpg",
    "https://i.imgur.com/fhUbwy6.jpg", "https://i.imgur.com/FlRylsY.jpg",
    "https://i.imgur.com/wHOPtRW.jpg", "https://i.imgur.com/S6J5ZEX.jpg",
    "https://i.imgur.com/2H9nodm.jpg", "https://i.imgur.com/PqIWVIz.jpg",
    "https://i.imgur.com/r7MIR8x.jpg", "https://i.imgur.com/ridLkYv.jpg",
    "https://i.imgur.com/J5P6sSa.jpg", "https://i.imgur.com/2ssF86m.jpg",
    "https://i.imgur.com/kc2AIq8.jpg",
]

# The master template (copy this from your first page)
MASTER_TEMPLATE = '''<!DOCTYPE html>
<html lang="en-US" prefix="og: https://ogp.me/ns#">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{TITLE}} | MULTIBET</title>
    <meta name="description" content="{{DESCRIPTION}}">
    
    <!-- Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;700&display=swap" rel="stylesheet">
    
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    
    <!-- Lucide Icons -->
    <script src="https://unpkg.com/lucide@latest"></script>
    
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    fontFamily: {
                        sans: ['Inter', 'sans-serif'],
                        display: ['Space Grotesk', 'sans-serif'],
                    },
                    colors: {
                        brand: {
                            red: '#f84643',
                            dark: '#0a0a0a',
                            gray: '#1a1a1a',
                            light: '#f5f5f5'
                        }
                    },
                    animation: {
                        'marquee': 'marquee 25s linear infinite',
                        'fade-in': 'fadeIn 0.6s ease-out',
                        'slide-up': 'slideUp 0.8s ease-out',
                    },
                    keyframes: {
                        marquee: {
                            '0%': { transform: 'translateX(0%)' },
                            '100%': { transform: 'translateX(-100%)' },
                        },
                        fadeIn: {
                            '0%': { opacity: '0' },
                            '100%': { opacity: '1' },
                        },
                        slideUp: {
                            '0%': { transform: 'translateY(20px)', opacity: '0' },
                            '100%': { transform: 'translateY(0)', opacity: '1' },
                        }
                    }
                }
            }
        }
    </script>
    
    <style>
        .gradient-text {
            background: linear-gradient(135deg, #f84643 0%, #ff6b6b 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .glass-effect {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .hover-lift {
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .hover-lift:hover {
            transform: translateY(-4px);
            box-shadow: 0 20px 40px rgba(248, 70, 67, 0.15);
        }
        
        .article-content p {
            margin-bottom: 1.5rem;
            line-height: 1.8;
            color: #374151;
        }
        
        .article-content h2 {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 1.875rem;
            font-weight: 700;
            margin-top: 2.5rem;
            margin-bottom: 1rem;
            color: #111827;
            scroll-margin-top: 100px;
        }
        
        .article-content h3 {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 1.5rem;
            font-weight: 700;
            margin-top: 2rem;
            margin-bottom: 1rem;
            color: #111827;
        }
        
        .article-content ul {
            margin-bottom: 1.5rem;
            padding-left: 1.5rem;
        }
        
        .article-content li {
            margin-bottom: 0.5rem;
            position: relative;
            padding-left: 1.5rem;
        }
        
        .article-content li::before {
            content: '';
            position: absolute;
            left: 0;
            top: 0.6rem;
            width: 6px;
            height: 6px;
            background: #f84643;
            border-radius: 50%;
        }
        
        .article-content ol {
            list-style: decimal;
            padding-left: 2rem;
            margin-bottom: 1.5rem;
        }
        
        .article-content blockquote {
            border-left: 4px solid #f84643;
            padding-left: 1.5rem;
            margin: 2rem 0;
            font-style: italic;
            color: #6b7280;
        }
        
        .article-content a {
            color: #f84643;
            font-weight: 600;
            text-decoration: underline;
            text-underline-offset: 3px;
        }
        
        .toc-link {
            position: relative;
            padding-left: 2rem;
        }
        
        .toc-link::before {
            content: attr(data-num);
            position: absolute;
            left: 0;
            top: 0;
            width: 1.5rem;
            height: 1.5rem;
            background: #f84643;
            color: white;
            border-radius: 50%;
            font-size: 0.75rem;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 600;
        }
        
        .reading-progress {
            position: fixed;
            top: 0;
            left: 0;
            height: 3px;
            background: linear-gradient(90deg, #f84643, #ff6b6b);
            z-index: 9999;
            transition: width 0.1s;
        }
    </style>
</head>
<body class="bg-gray-50 font-sans antialiased">
    <!-- Reading Progress Bar -->
    <div class="reading-progress" id="readingProgress"></div>
    
    <!-- Breaking News Ticker -->
    <div class="bg-brand-red text-white py-2 overflow-hidden relative">
        <div class="flex items-center max-w-7xl mx-auto px-4">
            <span class="flex items-center gap-2 font-bold text-sm uppercase tracking-wider shrink-0 mr-6">
                <i data-lucide="flame" class="w-4 h-4"></i>
                Hot News
            </span>
            <div class="overflow-hidden flex-1 relative">
                <div class="flex gap-8 animate-marquee whitespace-nowrap">
                    <a href="/mashemeji-lit-the-fuse-now-the-sportpesa-league-is-the-weekend-kenya-cant-ignore/" class="hover:underline text-sm">Mashemeji lit the fuse- Now the SportPesa League is the weekend Kenya can't ignore</a>
                    <span class="text-white/50">•</span>
                    <a href="/when-bundles-run-out-the-game-doesnt-stop-sportpesa-kenyas-ussd-casino-is-changing-how-kenyans-play/" class="hover:underline text-sm font-semibold">When bundles run out, the game doesn't stop- SportPesa Kenya's USSD Casino</a>
                    <span class="text-white/50">•</span>
                    <a href="/every-goal-can-pay-how-sportpesa-kenyas-goal-goal-and-1x2-markets-are-putting-instant-wins-in-fans-hands/" class="hover:underline text-sm">Every goal can pay- How SportPesa Kenya's Goal Goal and 1X2 markets</a>
                    <span class="text-white/50">•</span>
                    <a href="/from-99-bob-to-ksh-20-7m-nairobi-tailor-becomes-newest-sportpesa-mega-jackpot-winner/" class="hover:underline text-sm">From 99 bob to KSh 20.7M- Nairobi tailor becomes newest SportPesa Mega Jackpot winner</a>
                </div>
            </div>
        </div>
    </div>

    <!-- Header -->
    <header class="bg-white border-b border-gray-200 sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex items-center justify-between h-20">
                <!-- Logo -->
                <div class="flex items-center gap-3">
                    <a href="/" class="flex items-center gap-3 group">
                        <div class="w-12 h-12 bg-brand-red rounded-xl flex items-center justify-center transform group-hover:rotate-12 transition-transform">
                            <span class="text-white font-bold text-xl font-display">M</span>
                        </div>
                        <div>
                            <h1 class="text-2xl font-bold font-display text-gray-900 tracking-tight">MULTIBET</h1>
                            <p class="text-xs text-gray-500 uppercase tracking-widest">Your home of sportpesa mega jackpot</p>
                        </div>
                    </a>
                </div>

                <!-- Navigation -->
                <nav class="hidden md:flex items-center gap-8">
                    <a href="/" class="text-gray-700 hover:text-brand-red font-medium transition-colors">Home</a>
                    <a href="/category/reviews/" class="{{REVIEWS_ACTIVE}}">Reviews</a>
                    <a href="/category/predictions/" class="{{PREDICTIONS_ACTIVE}}">Predictions</a>
                    <a href="/category/news/" class="{{NEWS_ACTIVE}}">News</a>
                </nav>

                <!-- Actions -->
                <div class="flex items-center gap-4">
                    <div class="hidden md:flex items-center gap-3">
                        <a href="#" class="w-10 h-10 rounded-full bg-gray-100 flex items-center justify-center hover:bg-brand-red hover:text-white transition-all">
                            <i data-lucide="facebook" class="w-5 h-5"></i>
                        </a>
                        <a href="#" class="w-10 h-10 rounded-full bg-gray-100 flex items-center justify-center hover:bg-brand-red hover:text-white transition-all">
                            <i data-lucide="twitter" class="w-5 h-5"></i>
                        </a>
                        <a href="#" class="w-10 h-10 rounded-full bg-gray-100 flex items-center justify-center hover:bg-brand-red hover:text-white transition-all">
                            <i data-lucide="instagram" class="w-5 h-5"></i>
                        </a>
                    </div>
                    
                    <button onclick="toggleSearch()" class="w-10 h-10 rounded-full bg-gray-100 flex items-center justify-center hover:bg-brand-red hover:text-white transition-all">
                        <i data-lucide="search" class="w-5 h-5"></i>
                    </button>
                    
                    <button class="md:hidden w-10 h-10 rounded-full bg-gray-100 flex items-center justify-center">
                        <i data-lucide="menu" class="w-5 h-5"></i>
                    </button>
                </div>
            </div>
        </div>
        
        <!-- Search Overlay -->
        <div id="searchOverlay" class="hidden absolute top-full left-0 right-0 bg-white border-b border-gray-200 shadow-lg p-4 animate-fade-in">
            <div class="max-w-3xl mx-auto">
                <div class="relative">
                    <input type="search" placeholder="Search articles..." class="w-full pl-12 pr-4 py-3 rounded-xl border border-gray-200 focus:border-brand-red focus:ring-2 focus:ring-brand-red/20 outline-none transition-all">
                    <i data-lucide="search" class="w-5 h-5 text-gray-400 absolute left-4 top-1/2 -translate-y-1/2"></i>
                </div>
            </div>
        </div>
    </header>

    <!-- Secondary Header -->
    <div class="bg-gray-900 text-white py-3">
        <div class="max-w-7xl mx-auto px-4 flex items-center justify-between">
            <div class="flex items-center gap-4 text-sm">
                <button class="flex items-center gap-2 hover:text-brand-red transition-colors">
                    <i data-lucide="menu" class="w-4 h-4"></i>
                    <span class="hidden sm:inline">Menu</span>
                </button>
                <span class="text-gray-500">|</span>
                <span class="text-gray-300 flex items-center gap-2">
                    <i data-lucide="calendar" class="w-4 h-4"></i>
                    {{CURRENT_DATE}}
                </span>
            </div>
            <div class="flex items-center gap-4">
                <button onclick="toggleDarkMode()" class="flex items-center gap-2 text-sm hover:text-brand-red transition-colors">
                    <i data-lucide="moon" class="w-4 h-4"></i>
                    <span class="hidden sm:inline">Dark Mode</span>
                </button>
                <a href="/random/" class="flex items-center gap-2 text-sm hover:text-brand-red transition-colors">
                    <i data-lucide="shuffle" class="w-4 h-4"></i>
                    <span class="hidden sm:inline">Random</span>
                </a>
            </div>
        </div>
    </div>

    <!-- Breadcrumb -->
    <div class="max-w-7xl mx-auto px-4 py-4">
        <nav class="flex items-center gap-2 text-sm text-gray-500">
            <a href="/" class="hover:text-brand-red transition-colors">Home</a>
            <i data-lucide="chevron-right" class="w-4 h-4"></i>
            <a href="/category/{{CATEGORY_SLUG}}/" class="hover:text-brand-red transition-colors">{{CATEGORY_NAME}}</a>
            <i data-lucide="chevron-right" class="w-4 h-4"></i>
            <span class="text-gray-900 font-medium truncate max-w-xs sm:max-w-md">{{TITLE}}</span>
        </nav>
    </div>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto px-4 pb-16">
        <div class="grid lg:grid-cols-12 gap-8">
            <!-- Article Content -->
            <article class="lg:col-span-8 animate-slide-up">
                <!-- Category Badge -->
                <div class="mb-4">
                    <a href="/category/{{CATEGORY_SLUG}}/" class="inline-flex items-center gap-2 px-4 py-1.5 bg-brand-red/10 text-brand-red rounded-full text-sm font-semibold hover:bg-brand-red hover:text-white transition-all">
                        {{CATEGORY_NAME}}
                    </a>
                </div>

                <!-- Title -->
                <h1 class="text-3xl sm:text-4xl lg:text-5xl font-bold font-display text-gray-900 leading-tight mb-6">
                    {{TITLE}}
                </h1>

                <!-- Meta -->
                <div class="flex flex-wrap items-center gap-4 text-sm text-gray-500 mb-8 pb-8 border-b border-gray-200">
                    <div class="flex items-center gap-2">
                        <div class="w-8 h-8 rounded-full bg-brand-red flex items-center justify-center">
                            <i data-lucide="user" class="w-4 h-4 text-white"></i>
                        </div>
                        <span class="font-medium text-gray-900">multibet</span>
                    </div>
                    <span class="hidden sm:inline">•</span>
                    <div class="flex items-center gap-2">
                        <i data-lucide="calendar" class="w-4 h-4"></i>
                        <span>{{DATE}}</span>
                    </div>
                    <span class="hidden sm:inline">•</span>
                    <div class="flex items-center gap-2">
                        <i data-lucide="clock" class="w-4 h-4"></i>
                        <span>{{READ_TIME}} min read</span>
                    </div>
                </div>

                <!-- Featured Image -->
                <div class="relative mb-8 rounded-2xl overflow-hidden group">
                    <img src="{{IMAGE}}" alt="{{TITLE}}" class="w-full h-auto object-cover transform group-hover:scale-105 transition-transform duration-700">
                    <div class="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
                </div>

                {{TABLE_OF_CONTENTS}}

                <!-- Article Body -->
                <div class="article-content text-lg">
                    {{CONTENT}}
                </div>

                <!-- Share -->
                <div class="flex items-center justify-between py-6 border-t border-b border-gray-200 my-8">
                    <span class="font-semibold text-gray-900 flex items-center gap-2">
                        <i data-lucide="share-2" class="w-5 h-5"></i>
                        Share this Article
                    </span>
                    <div class="flex gap-3">
                        <a href="https://www.facebook.com/sharer/sharer.php?u={{CANONICAL_URL}}" target="_blank" class="w-10 h-10 rounded-full bg-blue-600 text-white flex items-center justify-center hover:scale-110 transition-transform">
                            <i data-lucide="facebook" class="w-5 h-5"></i>
                        </a>
                        <a href="https://twitter.com/intent/tweet?text={{TITLE}}&url={{CANONICAL_URL}}" target="_blank" class="w-10 h-10 rounded-full bg-gray-900 text-white flex items-center justify-center hover:scale-110 transition-transform">
                            <i data-lucide="twitter" class="w-5 h-5"></i>
                        </a>
                        <button onclick="copyLink()" class="w-10 h-10 rounded-full bg-gray-200 text-gray-700 flex items-center justify-center hover:scale-110 transition-transform relative" id="copyBtn">
                            <i data-lucide="link" class="w-5 h-5"></i>
                            <span id="copyTooltip" class="absolute -top-8 left-1/2 -translate-x-1/2 bg-gray-900 text-white text-xs px-2 py-1 rounded opacity-0 transition-opacity">Copied!</span>
                        </button>
                        <button onclick="window.print()" class="w-10 h-10 rounded-full bg-gray-200 text-gray-700 flex items-center justify-center hover:scale-110 transition-transform">
                            <i data-lucide="printer" class="w-5 h-5"></i>
                        </button>
                    </div>
                </div>

                <!-- Navigation -->
                <div class="grid sm:grid-cols-2 gap-4 mb-8">
                    {{PREVIOUS_POST}}
                    {{NEXT_POST}}
                </div>

                <!-- Author -->
                <div class="bg-gray-50 rounded-xl p-6 flex gap-4 items-start">
                    <div class="w-16 h-16 rounded-full bg-brand-red flex items-center justify-center shrink-0">
                        <span class="text-white font-bold text-xl font-display">M</span>
                    </div>
                    <div>
                        <a href="/author/multibet/" class="font-bold text-gray-900 hover:text-brand-red transition-colors">multibet</a>
                        <p class="text-sm text-gray-500 mt-1">Sports betting analyst and gaming industry expert covering the Kenyan market since 2018.</p>
                    </div>
                </div>
            </article>

            <!-- Sidebar -->
            <aside class="lg:col-span-4 space-y-6">
                <!-- Related Posts -->
                <div class="bg-white rounded-xl border border-gray-200 p-6">
                    <h3 class="font-display font-bold text-lg text-gray-900 mb-4 flex items-center gap-2">
                        <i data-lucide="newspaper" class="w-5 h-5 text-brand-red"></i>
                        Related Posts
                    </h3>
                    <div class="space-y-4">
                        {{RELATED_POSTS}}
                    </div>
                </div>

                <!-- Newsletter -->
                <div class="bg-gradient-to-br from-gray-900 to-gray-800 text-white rounded-xl p-6">
                    <h3 class="font-display font-bold text-lg mb-2">Stay Updated</h3>
                    <p class="text-gray-300 text-sm mb-4">Get the latest betting tips and news delivered to your inbox.</p>
                    <form class="space-y-3">
                        <input type="email" placeholder="Your email address" class="w-full px-4 py-2 rounded-lg bg-white/10 border border-white/20 text-white placeholder-gray-400 focus:outline-none focus:border-brand-red">
                        <button type="submit" class="w-full py-2 bg-brand-red hover:bg-red-600 rounded-lg font-semibold transition-colors">
                            Subscribe
                        </button>
                    </form>
                </div>

                <!-- Quick Links -->
                <div class="bg-white rounded-xl border border-gray-200 p-6">
                    <h3 class="font-display font-bold text-lg text-gray-900 mb-4">Quick Links</h3>
                    <nav class="space-y-2">
                        <a href="/" class="flex items-center justify-between p-3 rounded-lg hover:bg-gray-50 transition-colors group">
                            <span class="text-gray-700 group-hover:text-brand-red transition-colors">Home</span>
                            <i data-lucide="chevron-right" class="w-4 h-4 text-gray-400"></i>
                        </a>
                        <a href="/category/reviews/" class="flex items-center justify-between p-3 rounded-lg hover:bg-gray-50 transition-colors group">
                            <span class="text-gray-700 group-hover:text-brand-red transition-colors">Reviews</span>
                            <i data-lucide="chevron-right" class="w-4 h-4 text-gray-400"></i>
                        </a>
                        <a href="/category/predictions/" class="flex items-center justify-between p-3 rounded-lg hover:bg-gray-50 transition-colors group">
                            <span class="text-gray-700 group-hover:text-brand-red transition-colors">Predictions</span>
                            <i data-lucide="chevron-right" class="w-4 h-4 text-gray-400"></i>
                        </a>
                        <a href="/category/news/" class="flex items-center justify-between p-3 rounded-lg hover:bg-gray-50 transition-colors group">
                            <span class="text-gray-700 group-hover:text-brand-red transition-colors">News</span>
                            <i data-lucide="chevron-right" class="w-4 h-4 text-gray-400"></i>
                        </a>
                    </nav>
                </div>
            </aside>
        </div>
    </main>

    <!-- Footer -->
    <footer class="bg-gray-900 text-white pt-12 pb-6">
        <div class="max-w-7xl mx-auto px-4">
            <div class="grid md:grid-cols-4 gap-8 mb-8">
                <div>
                    <div class="flex items-center gap-3 mb-4">
                        <div class="w-10 h-10 bg-brand-red rounded-lg flex items-center justify-center">
                            <span class="text-white font-bold font-display">M</span>
                        </div>
                        <span class="text-xl font-bold font-display">MULTIBET</span>
                    </div>
                    <p class="text-gray-400 text-sm">Your trusted source for SportPesa Mega Jackpot predictions and betting insights in Kenya.</p>
                </div>
                <div>
                    <h4 class="font-semibold mb-4">Categories</h4>
                    <ul class="space-y-2 text-sm text-gray-400">
                        <li><a href="/category/reviews/" class="hover:text-brand-red transition-colors">Reviews</a></li>
                        <li><a href="/category/predictions/" class="hover:text-brand-red transition-colors">Predictions</a></li>
                        <li><a href="/category/news/" class="hover:text-brand-red transition-colors">News</a></li>
                        <li><a href="/category/tips/" class="hover:text-brand-red transition-colors">Betting Tips</a></li>
                    </ul>
                </div>
                <div>
                    <h4 class="font-semibold mb-4">Legal</h4>
                    <ul class="space-y-2 text-sm text-gray-400">
                        <li><a href="#" class="hover:text-brand-red transition-colors">Terms of Service</a></li>
                        <li><a href="#" class="hover:text-brand-red transition-colors">Privacy Policy</a></li>
                        <li><a href="#" class="hover:text-brand-red transition-colors">Responsible Gaming</a></li>
                        <li><a href="#" class="hover:text-brand-red transition-colors">18+ Only</a></li>
                    </ul>
                </div>
                <div>
                    <h4 class="font-semibold mb-4">Connect</h4>
                    <div class="flex gap-3">
                        <a href="#" class="w-10 h-10 rounded-full bg-white/10 flex items-center justify-center hover:bg-brand-red transition-colors">
                            <i data-lucide="facebook" class="w-5 h-5"></i>
                        </a>
                        <a href="#" class="w-10 h-10 rounded-full bg-white/10 flex items-center justify-center hover:bg-brand-red transition-colors">
                            <i data-lucide="twitter" class="w-5 h-5"></i>
                        </a>
                        <a href="#" class="w-10 h-10 rounded-full bg-white/10 flex items-center justify-center hover:bg-brand-red transition-colors">
                            <i data-lucide="instagram" class="w-5 h-5"></i>
                        </a>
                    </div>
                </div>
            </div>
            <div class="border-t border-gray-800 pt-6 flex flex-col md:flex-row items-center justify-between gap-4">
                <p class="text-sm text-gray-500">Copyright © 2026 MULTIBET | All Rights Reserved</p>
                <button onclick="scrollToTop()" class="flex items-center gap-2 text-sm text-gray-400 hover:text-brand-red transition-colors">
                    Back to Top
                    <i data-lucide="arrow-up" class="w-4 h-4"></i>
                </button>
            </div>
        </div>
    </footer>

    <script>
        lucide.createIcons();
        
        window.addEventListener('scroll', () => {
            const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
            const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
            const scrolled = (winScroll / height) * 100;
            document.getElementById('readingProgress').style.width = scrolled + "%";
        });
        
        function toggleSearch() {
            const overlay = document.getElementById('searchOverlay');
            overlay.classList.toggle('hidden');
            if (!overlay.classList.contains('hidden')) {
                overlay.querySelector('input').focus();
            }
        }
        
        function toggleToc() {
            const toc = document.getElementById('toc');
            if (toc) {
                const btn = event.target;
                if (toc.style.display === 'none') {
                    toc.style.display = 'block';
                    btn.textContent = 'Hide';
                } else {
                    toc.style.display = 'none';
                    btn.textContent = 'Show';
                }
            }
        }
        
        function copyLink() {
            navigator.clipboard.writeText(window.location.href);
            const tooltip = document.getElementById('copyTooltip');
            if (tooltip) {
                tooltip.style.opacity = '1';
                setTimeout(() => {
                    tooltip.style.opacity = '0';
                }, 2000);
            }
        }
        
        function scrollToTop() {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
        
        function toggleDarkMode() {
            document.body.classList.toggle('dark');
            const moonIcon = document.querySelector('[data-lucide="moon"]');
            if (moonIcon) {
                if (document.body.classList.contains('dark')) {
                    moonIcon.setAttribute('data-lucide', 'sun');
                } else {
                    moonIcon.setAttribute('data-lucide', 'moon');
                }
                lucide.createIcons();
            }
        }
        
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
            });
        });
    </script>
</body>
</html>'''

def extract_metadata(html):
    """Extract all metadata from the current page"""
    data = {
        'title': '',
        'description': '',
        'category_slug': 'reviews',
        'category_name': 'Reviews',
        'date': '',
        'image': '',
        'content': '',
        'read_time': '5'
    }
    
    # Extract title
    title_match = re.search(r'<title>(.*?)\s*\|\s*MULTIBET</title>', html)
    if title_match:
        data['title'] = title_match.group(1).strip()
    
    # Extract description
    desc_match = re.search(r'<meta name="description" content="([^"]*)"', html)
    if desc_match:
        data['description'] = desc_match.group(1)
    
    # Extract category
    cat_match = re.search(r'<a href="/category/([^/]+)/"[^>]*class="inline-flex[^>]*>([^<]+)</a>', html)
    if cat_match:
        data['category_slug'] = cat_match.group(1)
        data['category_name'] = cat_match.group(2)
    
    # Extract date
    date_match = re.search(r'<i data-lucide="calendar"[^>]*></i>\s*<span>([^<]+)</span>', html)
    if date_match:
        data['date'] = date_match.group(1).strip()
    
    # Extract image
    img_match = re.search(r'<img src="([^"]+)"[^>]*class="w-full h-auto object-cover', html)
    if img_match:
        data['image'] = img_match.group(1)
    
    # Extract ALL content between article tags
    article_match = re.search(r'<article[^>]*>(.*?)</article>', html, re.DOTALL)
    if article_match:
        article_content = article_match.group(1)
        
        # Remove the share section, navigation, and author box
        content_parts = re.split(r'<div class="flex items-center justify-between py-6 border-t', article_content, re.DOTALL)
        if len(content_parts) > 1:
            data['content'] = content_parts[0]
        else:
            data['content'] = article_content
        
        # Clean up the content
        data['content'] = re.sub(r'<div class="mb-4">.*?</div>', '', data['content'], flags=re.DOTALL)
        data['content'] = re.sub(r'<h1[^>]*>.*?</h1>', '', data['content'], flags=re.DOTALL)
        data['content'] = re.sub(r'<div class="flex flex-wrap items-center gap-4.*?</div>', '', data['content'], flags=re.DOTALL)
        data['content'] = re.sub(r'<div class="relative mb-8 rounded-2xl.*?</div>', '', data['content'], flags=re.DOTALL)
        data['content'] = data['content'].strip()
    
    # Extract read time
    read_time_match = re.search(r'<i data-lucide="clock"[^>]*></i>\s*<span>(\d+)\s*min read</span>', html)
    if read_time_match:
        data['read_time'] = read_time_match.group(1)
    
    return data

def extract_headings(content):
    """Extract h2 headings for TOC"""
    headings = re.findall(r'<h2[^>]*>(.*?)</h2>', content)
    return [re.sub(r'<[^>]+>', '', h).strip() for h in headings if h.strip()]

def add_heading_ids(content):
    """Add IDs to h2 headings"""
    def replace_h2(match):
        heading_text = re.sub(r'<[^>]+>', '', match.group(0)).strip()
        heading_id = re.sub(r'[^a-zA-Z0-9]+', '-', heading_text.lower()).strip('-')
        return f'<h2 id="{heading_id}">{heading_text}</h2>'
    
    return re.sub(r'<h2[^>]*>(.*?)</h2>', replace_h2, content, flags=re.DOTALL)

def generate_toc(headings):
    """Generate table of contents HTML"""
    if len(headings) < 2:
        return ''
    
    items = []
    for i, heading in enumerate(headings, 1):
        heading_id = re.sub(r'[^a-zA-Z0-9]+', '-', heading.lower()).strip('-')
        items.append(f'''
                <a href="#{heading_id}" class="toc-link block text-gray-700 hover:text-brand-red transition-colors text-sm font-medium" data-num="{i}">{heading}</a>''')
    
    return f'''
                <!-- Table of Contents -->
                <div class="bg-gray-50 rounded-xl p-6 my-8 border border-gray-200">
                    <div class="flex items-center justify-between mb-4">
                        <h3 class="font-display font-bold text-lg text-gray-900">Table of Contents</h3>
                        <button onclick="toggleToc()" class="text-sm text-brand-red font-medium hover:underline">Hide</button>
                    </div>
                    <nav id="toc" class="space-y-3">
                        {''.join(items)}
                    </nav>
                </div>'''

def get_all_pages():
    """Get all page slugs for navigation"""
    slugs = []
    for fp in sorted(glob.glob('**/*.html', recursive=True)):
        if fp in ('index.html', 'template.html') or '/category/' in fp.replace('\\', '/'):
            continue
        if fp.endswith('.html'):
            slug = fp.replace('.html', '').split('/')[-1]
            if slug and slug not in ('index', ''):
                slugs.append(slug)
    return slugs

def generate_prev_next(current_slug, all_slugs):
    """Generate previous/next post HTML"""
    if current_slug not in all_slugs:
        return '<div></div>', '<div></div>'
    
    idx = all_slugs.index(current_slug)
    prev_html = '<div></div>'
    next_html = '<div></div>'
    
    if idx > 0:
        prev_slug = all_slugs[idx - 1]
        prev_title = prev_slug.replace('-', ' ').title()
        prev_img = random.choice(IMGUR_IMAGES)
        prev_html = f'''
                <a href="/{prev_slug}/" class="group flex gap-4 p-4 rounded-xl border border-gray-200 hover:border-brand-red hover:shadow-lg transition-all">
                    <img src="{prev_img}" alt="Previous" class="w-20 h-20 object-cover rounded-lg shrink-0">
                    <div>
                        <span class="text-xs text-brand-red font-semibold uppercase flex items-center gap-1 mb-1">
                            <i data-lucide="arrow-left" class="w-3 h-3"></i>
                            Previous
                        </span>
                        <h4 class="font-semibold text-gray-900 line-clamp-2 group-hover:text-brand-red transition-colors">{prev_title}</h4>
                    </div>
                </a>'''
    
    if idx < len(all_slugs) - 1:
        next_slug = all_slugs[idx + 1]
        next_title = next_slug.replace('-', ' ').title()
        next_img = random.choice(IMGUR_IMAGES)
        next_html = f'''
                <a href="/{next_slug}/" class="group flex gap-4 p-4 rounded-xl border border-gray-200 hover:border-brand-red hover:shadow-lg transition-all text-right sm:text-left sm:flex-row-reverse">
                    <img src="{next_img}" alt="Next" class="w-20 h-20 object-cover rounded-lg shrink-0">
                    <div>
                        <span class="text-xs text-brand-red font-semibold uppercase flex items-center gap-1 mb-1 sm:justify-end">
                            Next
                            <i data-lucide="arrow-right" class="w-3 h-3"></i>
                        </span>
                        <h4 class="font-semibold text-gray-900 line-clamp-2 group-hover:text-brand-red transition-colors">{next_title}</h4>
                    </div>
                </a>'''
    
    return prev_html, next_html

def generate_related(current_slug, all_slugs):
    """Generate related posts HTML"""
    others = [s for s in all_slugs if s != current_slug]
    if not others:
        return '<p class="text-gray-500">No related posts</p>'
    
    picks = random.sample(others, min(3, len(others)))
    items = []
    for slug in picks:
        title = slug.replace('-', ' ').title()
        img = random.choice(IMGUR_IMAGES)
        items.append(f'''
                        <a href="/{slug}/" class="group flex gap-3">
                            <img src="{img}" alt="" class="w-20 h-14 object-cover rounded-lg shrink-0">
                            <div>
                                <h4 class="text-sm font-semibold text-gray-900 line-clamp-2 group-hover:text-brand-red transition-colors">{title}</h4>
                                <span class="text-xs text-gray-500">Latest</span>
                            </div>
                        </a>''')
    
    return '\n'.join(items)

def build_page(data, toc_html, prev_html, next_html, related_html, current_slug):
    """Build the final HTML page"""
    html = MASTER_TEMPLATE
    
    # Determine active navigation class
    reviews_active = 'text-brand-red font-semibold' if data['category_slug'] == 'reviews' else 'text-gray-700 hover:text-brand-red font-medium transition-colors'
    predictions_active = 'text-brand-red font-semibold' if data['category_slug'] == 'predictions' else 'text-gray-700 hover:text-brand-red font-medium transition-colors'
    news_active = 'text-brand-red font-semibold' if data['category_slug'] == 'news' else 'text-gray-700 hover:text-brand-red font-medium transition-colors'
    
    replacements = {
        '{{TITLE}}': data['title'],
        '{{DESCRIPTION}}': data['description'],
        '{{CATEGORY_SLUG}}': data['category_slug'],
        '{{CATEGORY_NAME}}': data['category_name'],
        '{{DATE}}': data['date'],
        '{{IMAGE}}': data['image'],
        '{{CONTENT}}': add_heading_ids(data['content']),
        '{{TABLE_OF_CONTENTS}}': toc_html,
        '{{PREVIOUS_POST}}': prev_html,
        '{{NEXT_POST}}': next_html,
        '{{RELATED_POSTS}}': related_html,
        '{{READ_TIME}}': data['read_time'],
        '{{CURRENT_DATE}}': datetime.now().strftime('%A, %B %d, %Y'),
        '{{CANONICAL_URL}}': f'/{current_slug}/',
        '{{REVIEWS_ACTIVE}}': reviews_active,
        '{{PREDICTIONS_ACTIVE}}': predictions_active,
        '{{NEWS_ACTIVE}}': news_active,
    }
    
    for key, value in replacements.items():
        html = html.replace(key, value)
    
    return html

def main():
    print("=" * 60)
    print("MULTIBET Page Converter - Fixed Version")
    print("=" * 60)
    
    # Get all pages for navigation
    all_slugs = get_all_pages()
    print(f"📄 Found {len(all_slugs)} pages for navigation")
    
    # Process all HTML files
    processed = 0
    errors = 0
    
    for filepath in sorted(glob.glob('**/*.html', recursive=True)):
        # Skip template and category pages
        if filepath in ('template.html', 'index.html') or '/category/' in filepath.replace('\\', '/'):
            continue
        
        # Get slug
        slug = filepath.replace('.html', '').split('/')[-1]
        if not slug or slug in ('index', ''):
            continue
        
        print(f"\n🔄 Processing: {filepath} (slug: {slug})")
        
        try:
            # Read file
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                html = f.read()
            
            # Create backup
            backup_path = filepath + '.backup'
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(html)
            
            # Extract metadata
            data = extract_metadata(html)
            
            # Generate components
            headings = extract_headings(data['content'])
            toc_html = generate_toc(headings)
            prev_html, next_html = generate_prev_next(slug, all_slugs)
            related_html = generate_related(slug, all_slugs)
            
            # Build new page
            new_html = build_page(data, toc_html, prev_html, next_html, related_html, slug)
            
            # Write new file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_html)
            
            processed += 1
            print(f"  ✅ Updated: {data['title'][:50]}...")
            if headings:
                print(f"     Found {len(headings)} headings for TOC")
            
        except Exception as e:
            errors += 1
            print(f"  ❌ Error: {str(e)}")
    
    print("\n" + "=" * 60)
    print(f"✅ Conversion Complete!")
    print(f"   Processed: {processed}")
    print(f"   Errors: {errors}")
    print(f"   Backup files created with .backup extension")
    print("=" * 60)

if __name__ == '__main__':
    main()
