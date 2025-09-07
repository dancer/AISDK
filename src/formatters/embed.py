import discord

def formatpr(pr):
    import re
    
    body = pr.get('body', '')
    
    if body:
        clean_body = re.sub(r'<!--.*?-->', '', body, flags=re.DOTALL)
        clean_body = re.sub(r'\n\s*\n+', '\n\n', clean_body)
        clean_body = clean_body.strip()
        
        if '## Summary' in clean_body:
            summary = clean_body.split('## Summary')[1].split('##')[0].strip()[:200]
            description = summary
        elif clean_body:
            lines = [line for line in clean_body.split('\n') if line.strip() and not line.startswith('#')]
            description = '\n'.join(lines[:3])[:200]
        else:
            description = None
    else:
        description = None
    
    embed = discord.Embed(
        title=f"{pr['title']}",
        url=pr['html_url'],
        description=description if description else None,
        color=0xFFFFFF
    )
    
    embed.set_author(
        name=f"{pr['user']['login']} opened PR #{pr['number']}",
        icon_url=pr['user']['avatar_url'],
        url=pr['user']['html_url']
    )
    
    embed.set_thumbnail(url=pr['user']['avatar_url'])
    
    if pr.get('merged'):
        status = 'merged'
    elif pr['state'] == 'closed':
        status = 'closed'
    else:
        status = 'open'
    
    fields = []
    fields.append(('status', status))
    
    if 'base' in pr and 'head' in pr:
        fields.append(('branch', f'{pr["head"]["ref"]} → {pr["base"]["ref"]}'))
    
    if pr.get('commits'):
        fields.append(('commits', str(pr['commits'])))
    
    if pr.get('additions') or pr.get('deletions'):
        fields.append(('changes', f'+{pr.get("additions", 0)} -{pr.get("deletions", 0)}'))
    
    for name, value in fields[:3]:
        embed.add_field(name=name, value=value, inline=True)
    
    return embed

def formatissue(issue):
    import re
    
    body = issue['body'] if issue['body'] else ''
    
    if body:
        image_pattern = r'<img[^>]+src="([^"]+)"[^>]*>'
        md_image_pattern = r'!\[.*?\]\((https?://[^\s\)]+)\)'
        
        images = re.findall(image_pattern, body)
        if not images:
            images = re.findall(md_image_pattern, body)
        
        clean_body = re.sub(image_pattern, '', body)
        clean_body = re.sub(md_image_pattern, '', clean_body)
        clean_body = re.sub(r'<[^>]+>', '', clean_body)
        clean_body = re.sub(r'\n\s*\n+', '\n\n', clean_body)
        clean_body = clean_body.strip()
        
        description = clean_body[:500] if clean_body else 'No description'
    else:
        description = 'No description'
        images = []
    
    embed = discord.Embed(
        title=f"Issue #{issue['number']}: {issue['title']}",
        url=issue['html_url'],
        description=description,
        color=0xFFFFFF
    )
    
    if images:
        embed.set_image(url=images[0])
    
    embed.set_author(name=issue['user']['login'], icon_url=issue['user']['avatar_url'], url=issue['user']['html_url'])
    embed.add_field(name='State', value=issue['state'], inline=True)
    if issue['labels']:
        labels = ', '.join([label['name'] for label in issue['labels']])
        embed.add_field(name='Labels', value=labels, inline=True)
    return embed

def formatrelease(release):
    import re
    
    body = release.get('body', '')
    description = None
    
    if body:
        lines = body.split('\n')
        changes = []
        capture = False
        
        for line in lines:
            if '## patch' in line.lower() or '## minor' in line.lower() or '## major' in line.lower():
                capture = True
                continue
            elif line.startswith('##') and capture:
                break
            elif capture and line.strip():
                if line.strip().startswith('-'):
                    changes.append(line.strip())
        
        if changes:
            description = '\n'.join(changes[:10])
        else:
            clean_body = re.sub(r'<!--.*?-->', '', body, flags=re.DOTALL)
            clean_body = re.sub(r'\n\s*\n+', '\n', clean_body)
            description = clean_body[:500]
    
    embed = discord.Embed(
        title=f"Release: {release['name'] or release['tag_name']}",
        url=release['html_url'],
        description=description if description else None,
        color=0xFFFFFF
    )
    embed.set_author(name=release['author']['login'], icon_url=release['author']['avatar_url'], url=release['author']['html_url'])
    embed.add_field(name='Tag', value=release['tag_name'], inline=True)
    if release['prerelease']:
        embed.add_field(name='Type', value='Prerelease', inline=True)
    else:
        embed.add_field(name='Type', value='Latest', inline=True)
    if 'published_at' in release:
        datetime_str = release['published_at'].replace('T', ' ').replace('Z', ' UTC')
        embed.add_field(name='Published', value=datetime_str, inline=True)
    return embed

def formatnpm(version, data):
    embed = discord.Embed(
        title=f"NPM Package Update: ai@{version}",
        url=f"https://www.npmjs.com/package/ai/v/{version}",
        description=data.get('description', 'No description'),
        color=0xFFFFFF
    )
    if 'dependencies' in data:
        deps = list(data['dependencies'].keys())[:5]
        embed.add_field(name='Dependencies', value=', '.join(deps), inline=False)
    return embed