/* Phono PEG Grammar
 * Copyright (C) 2004, 2005; 2016 Tiago Tresoldi
 */

/* first symbol, collects all rules in the given grammar */
rules =
    r:rule+ { return r; }

/* a single rule */
rule =
   _s "RULE" sep id:[-_.a-zA-Z0-9]+
   _s d:directives
   _s "END" sep _s
       { return { id:         id.join(''),
                  directives: d
                };
       }

/* Collection of directives that make up a rule */
directives = 
    _s d:directive+ _s { return d; }

/* comments, c-style, only single lines */
/* the final _s here allows for blank lines between comments */
_c =
    [\t ]* "//" [^\n]* "\n" _s

/* spaces, ignored */
_s =
    _c _s /
    [\r\n\t ]*

/* optional separator between commands and values */
sep =
    _s ":"? _s

/* separator for features */
feat_sep =
   _s "," _s

/* index, rule takes any string and converts */
index =
    digits:[-+0-9]+ { return parseInt(digits.join(""), 10); }

/* directive */
directive = 
    cmd:command p:position _s args:args _s  {
        return { command: cmd,
                 position: p,
                 args: args};
    }

/* commands for rules */
command =
    "IF" sep   { return "if"; } /
    "THEN" sep { return "then"; }

/* position for command, fixed or relative */
position =
        i:index { return ["fix", i]; } /
    "i" i:index { return ["rel", i]; } /
    "i"         { return ["rel", 0]; }

/* arguments, either features or ipa strings */
args =
    f:features            { return {type: "features", value: f }; } /
    ipa:ipa _s f:features { return {type: "specific",
                                    value: {ipa: ipa, features: f}}; } /
    ipa:ipa               { return {type: "ipa",      value: ipa}; }
   
ipa =
    "/" ipa:[^/]+ "/" { return ipa.join(""); }


/* after chomsky and halle features */
features =
    f:feature feat_sep fs:features {
        fs.push(f); return fs;
    } /
    f:feature { return [f]; }

/* matches a feature */
feature =
    op:operator id:[-_.a-z]+ { return op + id.join(''); }

/* operators for features: "-" negates, "+" sets, "!" sets the
 * opposite, "~" deletes */
operator =
    [-+!~]

