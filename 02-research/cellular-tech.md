# Cellular Technologies

## Cell Towers

The local "hub" in a mobile network that connects a cellular device to the cellular network
- This is our entry point into the cellular/global networks

### How cell towers work

Signal transmission and reception
- The antennas mounted on the tower send radio waves to devices in the surrounding area and receive signals back

Backhaul connection
- The tower connects to the core mobile network with fiber, microwave, or other links to forward voice, data, and control signals

Network coordination and hand-off management
- Cell towers work in sync with neighboring towers like a mesh topology
- When you leave one tower bubble, the network transfers your connection to the next tower without interrupting your call or stream

Enhanced 911 location data
- Cell towers also provide enhanced 911 location data during emergencies, allowing emergency responders to more accurately pinpoint your location
- Think about what else that could mean

### Cell tower components

Antennas
- Transmit (downlink) and receive (uplink) signals
- Typically arranged in a sectorized pattern

Transceivers and radios
- Equipment that generates, converts, and processes RF signals

Backhaul links
- Fiber, microwave dishes, or other links that carry data between the site and the core network

Power supply and backup
- Towers rely on stable power and often have backup batteries or generators for outages

Structural support and grounding
- The tower itself, lightning protection, and grounding systems ensure safety and reliability

Ref:
- https://www.t-mobile.com/dialed-in/wireless/what-is-a-cell-tower

# Global System for Mobiles (GSM)

- The original 2G standard (1991)

- Initially based on time division
  - Calls take turns using the RF signal

- Worldwide option, first introduced in Europe
  - Making it easier to travel with a GSM phone
  - Most of the world is covered in GSM

- Connected devices authenticate with SIM cards
  - Authenticates the SIM cards, not the device
  
# Subscriber Identity Module (SIM) Cards

- Introduced with GSM

- Identify and authenticate devices and maintain a connection to the network
  - This allows users to use devices in different countries without necessarily changing the phone number
  
- Allows users to easily transfer information into a new device by moving the SIM card and roaming between different GSM networks across the globe

# Code Division Multiple Access (CDMA)

- Mostly a US thing for now

- Based on encoding multiple connections with unique identifiers and then decoding them on the receiving end
  - MEID or ESN number
  - Authenticates the device itself

- Known for its high call quality and reliability, as well as its ability to support high-speed data services

- Some devices are dual band, meaning GSM and CDMA capabilities

Ref:
- https://www.t-mobile.com/dialed-in/wireless/gsm-vs-cdma-what-you-need-to-know-about-phone-bands

# 1G

- First generation of GSM
- Analog technology

# 2G

- Second gen
- Digital technology
- Both GSM and CDMA versions

# 3G

- Third gen
- Increased transfer rates

# High Speed Packet Access (HSPA)

Merge of two technologies
- High Speed Downlink Packet Access (HSDPA)
- High Speed Uplink Packet Access (HSUPA)

- Improves the performance of existing 3G networks

Ref:
- https://everything.explained.today/High_Speed_Packet_Access/

# 4G

- You guessed it, fourth gen

- Higher data rates than 3G, lower latency

- IP based network
  - Packet switching architecture, easier integration with the internet

# Long Term Evolution (LTE)

- 4th Gen technology, often called 4G LTE
  - Increases bandwidth available for voice and data communications by using a different radio interface combined with a number of network improvements
  
- The upgrade path for both GSM and CDMA based networks

- Circuit based network

# Advanced Wireless Services (AWS)

Not that AWS

- Also referred to as UMTS band IV

- Uses microwave frequencies in two segments: from 1710 to 1755 MHz for uplink, and from 2110 to 2155 MHz for downlink

Ref:
- https://everything.explained.today/Advanced_Wireless_Services/

# XLTE

- Provides a minimum of double the bandwidth of LTE

- XLTE ready devices automatically access both the 700 Mhz and the AWS spectrum in XLTE cities

# VoLTE

- Voice technology that works over the LTE data connection rather than 3G voice bands
  - Very high voice quality
  
- Both participants need to be using it

- Has the ability to make video calls

# Wifi Calling

- What could this possibly be?
  - Hint it uses the internet for voice calls as opposed to a phone company's network

- Promises the ability to swap seamlessly between Wi-Fi and wireless phone networks

# Roaming

Data roaming is the use of cellular data services on a mobile device outside of the coverage area of the home network

Domestic roaming
- When you're still within your provider’s home country, but your phone connects to a different partner network due to limited coverage in your area
- Typically doesn’t come with extra charges, so it's usually seamless and worry-free

International roaming
- When you leave your home country and your carrier relies on agreements with foreign networks to keep you connected
- Can rack up significant fees for data, calls, and texts, often at much higher rates than you’d pay at home

Ref:
- https://www.t-mobile.com/dialed-in/wireless/what-is-data-roaming

# Notes

- Cell towers are usually leased from tower companies, a practice known as “collocation”
  - Each carrier installs its own antennas, radios, and backhaul links
  
Other refs:
- https://danielmiessler.com/blog/cellular