# New templatized version of the Old Fashioned newsletter

newsletter_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{newsletter_name}</title>
    <style>
        /* Base styles with explicit colors for dark mode compatibility */
        @import url('https://fonts.googleapis.com/css2?family=Berkshire+Swash&family=IM+Fell+English:ital@0;1&family=Playfair+Display:ital,wght@0,400;0,700;1,400&display=swap');
        
        body {{
            font-family: 'IM Fell English', Georgia, 'Times New Roman', Times, serif;
            line-height: 1.5;
            color: #1a1308 !important; /* Darkened for better contrast */
            background-color: #f5eee1 !important;
            margin: 0;
            padding: 0;
        }}
        
        .container {{
            max-width: 800px;
            margin: 0 auto;
            padding: 25px;
            background: #f8f4e9 !important; /* Simplified gradient to solid color */
            border: 8px double #9b8c70;
            box-shadow: 0 4px 12px rgba(104, 86, 52, 0.15);
        }}
        
        /* Header styles with vintage feel */
        .header {{
            text-align: center;
            margin-bottom: 20px;
            position: relative;
        }}
        
        .decorative {{
            font-size: 18px;
            color: #4d4026 !important; /* Darkened for better contrast */
            margin: 0 0 15px 0;
            font-weight: bold;
        }}
        
        .decorative:before, .decorative:after {{
            content: "✦";
            display: inline-block;
            margin: 0 10px;
        }}
        
        .newsletter-title {{
            font-family: 'Berkshire Swash', cursive;
            font-size: 54px;
            font-weight: 400;
            margin: 0;
            line-height: 1.2;
            color: #3b2814 !important; /* Darkened for better contrast */
            text-transform: none;
            padding: 10px 0;
            position: relative;
        }}
        
        .date {{
            font-family: 'IM Fell English', Georgia, serif;
            margin: 15px 0 10px;
            font-size: 16px;
            color: #4d4026 !important; /* Darkened for better contrast */
            font-style: italic;
            font-weight: bold;
        }}
        
        .summary {{
            font-family: 'IM Fell English', Georgia, serif;
            font-size: 18px;
            font-style: italic;
            margin: 15px 0 25px;
            color: #4d4026 !important; /* Darkened for better contrast */
            padding: 0 20px;
            position: relative;
            font-weight: bold;
        }}
        
        .summary:before, .summary:after {{
            content: "~";
            position: absolute;
            top: 50%;
            font-size: 20px;
            color: #7d7250 !important; /* Darkened for better contrast */
        }}
        
        .summary:before {{
            left: 0;
        }}
        
        .summary:after {{
            right: 0;
        }}
        
        /* Decorative vintage elements */
        .vintage-ornament {{
            text-align: center;
            margin: 15px 0;
            color: #7d7250 !important; /* Darkened for better contrast */
            font-size: 24px;
            line-height: 1;
            font-weight: bold;
        }}
        
        /* Article styles */
        .article {{
            margin-bottom: 15px;
            overflow: hidden;
            padding-bottom: 15px;
            position: relative;
            color: #1a1308 !important; /* Darkened for better contrast */
        }}
        
        /* Replaced with actual HTML divider - see HTML structure below */
        .article-divider {{
            text-align: center;
            color: #7d7250 !important;
            font-size: 16px;
            margin: 10px 0;
            font-weight: bold;
            letter-spacing: 8px;
        }}
        
        .article-title {{
            font-family: 'Playfair Display', Georgia, serif;
            font-size: 26px;
            margin-bottom: 10px;
            font-weight: bold;
            color: #3b2814 !important; /* Darkened for better contrast */
            text-decoration: none;
            line-height: 1.3;
        }}
        
        .article-title a {{
            color: #3b2814 !important; /* Darkened for better contrast */
            text-decoration: none;
            position: relative;
            display: inline-block;
        }}
        
        .article-title a:hover {{
            text-decoration: none;
        }}
        
        .article-title a:hover:after {{
            content: "";
            position: absolute;
            bottom: 2px;
            left: 0;
            width: 100%;
            height: 3px;
            background: linear-gradient(to right, transparent, rgba(155, 140, 112, 0.5), transparent);
        }}
        
        .article-summary {{
            font-family: 'IM Fell English', Georgia, serif;
            font-size: 16px;
            line-height: 1.7;
            color: #1a1308 !important; /* Darkened for better contrast */
        }}
        
        .footer {{
            text-align: center;
            font-family: 'IM Fell English', Georgia, serif;
            font-size: 14px;
            margin-top: 30px;
            color: #4d4026 !important; /* Darkened for better contrast */
            font-style: italic;
            font-weight: bold;
        }}
        
        /* Force text colors even on dark mode */
        * {{
            color-scheme: light !important;
            -webkit-text-fill-color: inherit !important;
        }}
        
        /* Responsive styles */
        @media screen and (max-width: 480px) {{
            .container {{
                padding: 15px;
            }}
            
            .newsletter-title {{
                font-size: 42px;
            }}
            
            .article-title {{
                font-size: 22px;
            }}
            
            /* Additional mobile-specific contrast improvements */
            body, .article, .article-summary {{
                color: #000000 !important; /* Even darker for mobile */
            }}
            
            .article-title, .article-title a, .newsletter-title {{
                color: #301f0f !important; /* Even darker for mobile */
            }}
            
            .decorative, .date, .summary, .footer {{
                color: #3d3317 !important; /* Even darker for mobile */
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <p class="decorative">Est. 2025</p>
            <h1 class="newsletter-title">{newsletter_name}</h1>
            <p class="date">{formatted_date}</p>
            <p class="summary">{newsletter_title}</p>
        </div>
        
        <div class="vintage-ornament">❧</div>
        
        <!-- Main content -->
        <div class="content">
            {articles}
        </div>
        
        <div class="vintage-ornament">✧</div>
        
        <!-- Footer -->
        <div class="footer">
            <p>Curated with care for the discerning collector</p>
        </div>
    </div>
</body>
</html>
"""

article_template = """
<div class="article">
    <h2 class="article-title"><a href="{link}">{title}</a></h2>
    <p class="article-summary">{summary}</p>
</div>
<div class="article-divider">✦ ✦ ✦</div>
"""

last_article_template = """
<div class="article">
    <h2 class="article-title"><a href="{link}">{title}</a></h2>
    <p class="article-summary">{summary}</p>
</div>
"""