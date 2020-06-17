![Capture d’écran 2019-12-05 à 14 50 00](https://user-images.githubusercontent.com/9840435/70241068-ab89d600-176e-11ea-9340-aeb9ee7d3ac7.jpg)

Hi!
As said in #176, I added functionalty to add funding url. Right now it only use URL, (without 'type' field) but if You want I can implement it too :)
Secondly I wasn't sure how this URL should look like in ReadME, that's why I'm open to potential new requirements.

Regards,
Mikolaj
https://blog.opencollective.com/beyond-post-install/


User should be able to choose among a list of different README templates. These templates would use  the same project infos (or part of them) and display them in a different way.
Fix  #146
**Is your feature request related to a problem? Please describe.**
When author asked I've had 2 author with a comma, the result was broken.

**Describe the solution you'd like**
If I provide two author separated with a comme it must create 2 lines.

**Describe alternatives you've considered**
comma, semi-colon, no preference, but precise it in the question maybe

(great project btw, you da best)
For old guys like me, that still develop with Maven, it would be great to generate the README.md from a pom.xml instead of a package.json file.

* New command line option: `-x`
```bash
readme -x
```

* The `pom.xml` must contain some informations such as:
```xml
<project>
    <name>My Great Project</name>
    <description>Some useful description</description>
    <url>http://example.com</url>

    <contributors>
        <contributor>
            <name>Bob</name>
        </contributor>
    </contributors>

    <licenses>
        <license>
            <name>MIT</name>
        </license>
    </licenses>

    <issueManagement>
        <url>http://example.com/issues</url>
    </issueManagement>
</project>
```

Split `readme-md-generator` into multiple packages ang manage them with `yarn workspaces`. Each question would be a plugin that you can easily register. 
You should publish a thin wrapper package named `create-markdown-md` with a small bin script. Due to the `create-*` convention it would qualify as a proper "initializer package".
This would allow usage via `npm init readme-md` or `yarn create readme-md` without prior installation.

I'd even go further and name it `create-readme.md` for a totally awesome `yarn create readme.md` :)