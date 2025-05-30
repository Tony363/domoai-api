import discord
import os
import asyncio
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

async def test_discord_credentials():
    """Test Discord credentials from .env file"""
    
    # Get credentials from environment
    token = os.getenv('DISCORD_TOKEN')
    guild_id = os.getenv('DISCORD_GUILD_ID')
    channel_id = os.getenv('DISCORD_CHANNEL_ID')
    
    print("=" * 60)
    print("DISCORD CREDENTIALS TEST")
    print("=" * 60)
    
    # Check if credentials exist
    print("\n1. Checking if credentials are loaded from .env:")
    print(f"   - Token: {'✓ Found' if token else '✗ Not found'}")
    print(f"   - Guild ID: {'✓ Found' if guild_id else '✗ Not found'}")
    print(f"   - Channel ID: {'✓ Found' if channel_id else '✗ Not found'}")
    
    if not all([token, guild_id, channel_id]):
        print("\n❌ Missing credentials. Please check your .env file.")
        return
    
    # Create Discord client with necessary intents
    intents = discord.Intents.default()
    intents.guilds = True
    intents.messages = True
    client = discord.Client(intents=intents)
    
    # Store test results
    test_results = {
        'login': False,
        'guild': False,
        'channel': False,
        'guild_name': None,
        'channel_name': None,
        'bot_name': None
    }
    
    @client.event
    async def on_ready():
        print(f"\n2. Testing Discord Token:")
        print(f"   ✓ Successfully logged in as: {client.user}")
        test_results['login'] = True
        test_results['bot_name'] = str(client.user)
        
        # Test Guild ID
        print(f"\n3. Testing Guild ID ({guild_id}):")
        try:
            guild = client.get_guild(int(guild_id))
            if guild:
                print(f"   ✓ Guild found: {guild.name}")
                test_results['guild'] = True
                test_results['guild_name'] = guild.name
                
                # Test Channel ID
                print(f"\n4. Testing Channel ID ({channel_id}):")
                try:
                    channel = guild.get_channel(int(channel_id))
                    if channel:
                        print(f"   ✓ Channel found: #{channel.name}")
                        test_results['channel'] = True
                        test_results['channel_name'] = channel.name
                        
                        # Check channel permissions
                        permissions = channel.permissions_for(guild.me)
                        print(f"\n5. Channel Permissions:")
                        print(f"   - Read Messages: {'✓' if permissions.read_messages else '✗'}")
                        print(f"   - Send Messages: {'✓' if permissions.send_messages else '✗'}")
                        print(f"   - Read Message History: {'✓' if permissions.read_message_history else '✗'}")
                    else:
                        print(f"   ✗ Channel not found in guild")
                        print(f"   Note: Make sure the channel ID belongs to the specified guild")
                except ValueError:
                    print(f"   ✗ Invalid channel ID format")
                except Exception as e:
                    print(f"   ✗ Error accessing channel: {e}")
            else:
                print(f"   ✗ Guild not found")
                print(f"   Note: Make sure the bot is a member of this guild")
        except ValueError:
            print(f"   ✗ Invalid guild ID format")
        except Exception as e:
            print(f"   ✗ Error accessing guild: {e}")
        
        # Close the client
        await client.close()
    
    # Try to run the client
    try:
        print("\nConnecting to Discord...")
        await client.start(token)
    except discord.LoginFailure:
        print("\n❌ Failed to login: Invalid Discord token")
        print("   Please check if the token is correct and not expired")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Token Valid: {'✓ Yes' if test_results['login'] else '✗ No'}")
    print(f"Guild Access: {'✓ Yes' if test_results['guild'] else '✗ No'}")
    print(f"Channel Access: {'✓ Yes' if test_results['channel'] else '✗ No'}")
    
    if all([test_results['login'], test_results['guild'], test_results['channel']]):
        print("\n✅ All credentials are valid and working!")
    else:
        print("\n⚠️  Some credentials need attention. See details above.")

if __name__ == '__main__':
    # Run the async test function
    asyncio.run(test_discord_credentials())
