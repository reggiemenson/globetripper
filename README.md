
# GlobeTripper

This maintenance and refactoring project is based on an initial team project called [TripBit](https://github.com/reggiemenson/tripbit)
by [Michael Adair](https://github.com/mjadair), [Kathrin Eichinger](https://github.com/katheich), [Georg Preuss](https://github.com/georgpreuss) and [myself](https://github.com/reggiemenson).


## Overview

TripBit is a small project inspired by analogue scratch maps, where people scratch out the countries they have visited. Users select the cities they have travelled to, are assigned a travel score and can earn badges for certain achievements. They can also create and join groups to compare their travels with friends more directly. All of this is achieved by using the Django REST framework with a PostgreSQL database and a React front-end.

You can launch the app on Heroku [here](https://tripbit4.herokuapp.com/), or find the GitHub repo [here](https://github.com/reggiemenson/tripbit).

## Table of contents

1. [Installation](#Installation)
2. [Routes](#Routes)
    - [Back-end](#Back-end)


## Installation

This application was developed with Python 3.7 and Node version 12. There has been a change from the usage of a Pipenv shell to a virtual environment.

To start the project first:

1. Create a virtual environment with:

```
python3.7 -m venv <path-name>
```

2. Start up the environment with:

```
source <path-name>/bin/activate
```

3. Install the required python packages with:

```
pip install -r requirements.txt
```

To begin the application you can now run for the back and frontend servers respectively:

```
npm run serve:backend
npm run serve:frontend
```

NB: Note that if a dist folder has been built, this may interfere with the development environment.


## Routes

### Back-end

**API End-points**

#### 1. User	

<table >
  <tr>
    <th></th>
    <th>GET</th>
    <th>POST</th>
    <th>PUT</th>
    <th>DELETE</th>
  </tr>
  <tr>
    <td>/register</td>
    <td></td>
    <td>X</td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td>/login</td>
    <td></td>
    <td>X</td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td>/users</td>
    <td>X</td>
    <td></td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td>/profile/&lt;int:pk&gt;</td>
    <td>X</td>
    <td></td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td>/profile</td>
    <td>X</td>
    <td></td>
    <td>X</td>
    <td>X</td>
  </tr>
  <tr>
    <td>/profile/edit/all</td>
    <td></td>
    <td></td>
    <td>X</td>
    <td></td>
  </tr>
</table>

- `/register` only has a post route, where the user's data is received and stored in the database.
- Similarly, `/login` only has a post route, where the user's login information is received, checked and, if valid, a JWT token is returned as response.
- `/users` is a simple GET route, that provides a full list of users to allow searching for other users to access their profiles.
- `/profile/<int:pk>/` similarly only has a GET route to fetch a specific user profile to be displayed.
- `/profile` has a GET, PUT and DELETE route, all relating to the user data of the user currently logged in, allowing them to respectively fetch, amend and delete their profile information.
- `/profile/edit/all` is the most complex part of the platform, even though it only involves a PUT route. This is the route via which a user adds towns that they have visited to their profile, setting off a chain-reaction:
  - The route is set up to always receive the full list of towns a given user has visited. These towns are added to the user in the database.
  - Given this list of towns, the badges that the user has earned are determined. This is done via bespoke functions for each type of badge in the database, for instance the 'Columbus badge' (with ID 209 in the database) is determined as follows:

    ```py
    all_user_countries = list(map(lambda town: town['country'], towns))
    unique_user_countries = set(all_user_countries)
    unique_continents = set(map(lambda town: town['continent'], towns))

    # Columbus (209)
    if 'Portugal' in unique_user_countries and 'Spain' in unique_user_countries and 'South America' in unique_continents:
        badge_ids.append(209)
    ```
  - Once this individual user's new badges have been allocated, the badges that rely on comparing information across users are re-assessed: checking which user has visited the most cities, countries, continents and earned the most badges. These users are saved to the badges directly.
  - Following this, we return to the individual user who posted new towns, whose score is now determined, adding 5 XP per town, 10 XP per capital, 20 XP per country and 50 XP per continent visited.
  - All of this new information is added to the user profile, which is then finally saved in the database.


#### 2. Town

<table >
  <tr>
    <th></th>
    <th>GET</th>
    <th>POST</th>
    <th>PUT</th>
    <th>DELETE</th>
  </tr>
  <tr>
    <td>/towns</td>
    <td>X</td>
    <td></td>
    <td></td>
    <td></td>
  </tr>
  </table>

- `/towns` only has a GET route, since the town data is only displayed and never amended directly. It was a conscious choice to have users only add towns they have visited via the `/profile/edit/all` route outlined above, in order to ensure that all the other information that depended on the list of towns would always be updated correctly.

#### 3. Badge

<table >
  <tr>
    <th></th>
    <th>GET</th>
    <th>POST</th>
    <th>PUT</th>
    <th>DELETE</th>
  </tr>
  <tr>
    <td>/badges</td>
    <td>X</td>
    <td></td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td>/badges/&lt;int:pk&gt;/</td>
    <td>X</td>
    <td></td>
    <td></td>
    <td></td>
  </tr>
  </table>

- `/badges` and `/badges/<int:pk>` similarly only involve simple GET routes, allowing the display of all badges, as well as of one specific badge at a time, since the badge information itself is immutable in our database and badges are allocated to users via the `/profile/edit/all` route outlined above. In fact, we did not end up using these routes at all.

#### 4. Group

<table >
  <tr>
    <th></th>
    <th>GET</th>
    <th>POST</th>
    <th>PUT</th>
    <th>DELETE</th>
  </tr>
  <tr>
    <td>/groups</td>
    <td>X</td>
    <td>X</td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td>/groups/&lt;int:pk&gt;/</td>
    <td>X</td>
    <td></td>
    <td>X</td>
    <td>X</td>
  </tr>
  <tr>
    <td>/groups/&lt;int:pk&gt;/membership</td>
    <td>X</td>
    <td></td>
    <td>X</td>
    <td>X</td>
  </tr>
  </table>

- `/groups` has both a GET and a POST route, the former allowing to see all group information in the database and the latter allowing the posting of a new group to the platform. The user who posted the group automatically becomes that group's owner.
- `/groups/<int:pk>` has a publicly accessible GET route, allowing the info of a specific group to be displayed. It also has a PUT and DELETE route, which allow the owner of the group to amend and delete the group information from the platform respectively.
- `/groups/<int:pk>/membership` similarly has a GET, PUT and DELETE route, which do the following:
  - The GET route allows any user not affiliated with the group to request membership of the group. This will add the user to the 'requests' field of the Group model.
  - The PUT route allows the owner of the group to specify the ID of one of the user's in the list of requests, which will approve that user's membership and move them to the 'members' field of the group.
  - The DELETE route allows a member to remove themselves from the group, or the owner of the group to remove a specific member from the group, again by specifying the ID of the member to be removed.
