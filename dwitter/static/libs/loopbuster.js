(function() {
  function v(u, r, c) {
    function k(a, m) {
      if (!r[a]) {
        if (!u[a]) {
          var h = "function" == typeof require && require;
          if (!m && h) return h(a, !0);
          if (n) return n(a, !0);
          h = Error("Cannot find module '" + a + "'");
          throw h.code = "MODULE_NOT_FOUND", h;
        }
        h = r[a] = {
          exports: {}
        };
        u[a][0].call(h.exports, function(h) {
          return k(u[a][1][h] || h)
        }, h, h.exports, v, u, r, c)
      }
      return r[a].exports
    }
    for (var n = "function" == typeof require && require, l = 0; l < c.length; l++) k(c[l]);
    return k
  }
  return v
})()({
  1: [function(v, u, r) {
    var c = v("esprima");
    window.instrument = function(k) {
      var n =
        1,
        l = [];
      try {
        c.parse(k, {
          range: !0,
          tolerant: !1,
          sourceType: "script",
          jsx: !0
        }, function(a) {
          switch (a.type) {
            case "DoWhileStatement":
            case "ForStatement":
            case "ForInStatement":
            case "ForOfStatement":
            case "WhileStatement":
              var m = 1 + a.body.range[0],
                h = a.body.range[1],
                c = "window.stopper.restartLoop(%d);if (window.stopper.testLoop(%d)){throw 'Frame timed out, paused dweet.';}".replace(/%d/g, n),
                e = "";
              "BlockStatement" !== a.body.type && (c = "{" + c, e = "\n}", --m);
              l.push({
                pos: m,
                str: c
              });
              l.push({
                pos: a.range[1],
                str: "\nwindow.stopper.exitLoop(%d);\n".replace("%d", n)
              });
              l.push({
                pos: h,
                str: e
              });
              ++n
          }
        });
      } catch (e) {
        // Parsing errors, ignore
      }
      l.sort(function(a,
        m) {
        return m.pos - a.pos
      }).forEach(function(a) {
        k = k.slice(0, a.pos) + a.str + k.slice(a.pos)
      });
      return k
    };
    r.handler = function(c, n) {
      try {
        "" === (c.markup || "") ? n.succeed({
          markup: ""
        }): n.succeed({
          markup: instrument(c.markup)
        })
      } catch (a) {
        var k = 1;
        try {
          k = a.lineNumber
        } catch (m) {}
        n.succeed({
          error: a.description,
          line: k
        })
      }
    }
  }, {
    esprima: 2
  }],
  2: [function(v, u, r) {
    (function(c, k) {
      "object" === typeof r && "object" === typeof u ? u.exports = k() : "function" === typeof define && define.amd ? define([], k) : "object" === typeof r ? r.esprima = k() : c.esprima = k()
    })(this,
      function() {
        return function(c) {
          function k(l) {
            if (n[l]) return n[l].exports;
            var a = n[l] = {
              exports: {},
              id: l,
              loaded: !1
            };
            c[l].call(a.exports, a, a.exports, k);
            a.loaded = !0;
            return a.exports
          }
          var n = {};
          k.m = c;
          k.c = n;
          k.p = "";
          return k(0)
        }([function(c, k, n) {
          var l = n(1),
            a = n(3),
            m = n(11),
            h = n(15);
          k.parse = function(h, e, g) {
            var f = null,
              b = function(b, d) {
                g && g(b, d);
                f && f.visit(b, d)
              },
              d = "function" === typeof g ? b : null,
              t = !1;
            if (e) {
              t = "boolean" === typeof e.comment && e.comment;
              var p = "boolean" === typeof e.attachComment && e.attachComment;
              if (t || p) f = new l.CommentHandler,
                f.attach = p, e.comment = !0, d = b
            }
            h = e && "boolean" === typeof e.jsx && e.jsx ? new m.JSXParser(h, e, d) : new a.Parser(h, e, d);
            e = h.parseProgram();
            t && (e.comments = f.comments);
            h.config.tokens && (e.tokens = h.tokens);
            h.config.tolerant && (e.errors = h.errorHandler.errors);
            return e
          };
          k.tokenize = function(a, e, g) {
            a = new h.Tokenizer(a, e);
            e = [];
            try {
              for (;;) {
                var f = a.getNextToken();
                if (!f) break;
                g && (f = g(f));
                e.push(f)
              }
            } catch (b) {
              a.errorHandler.tolerate(b)
            }
            a.errorHandler.tolerant && (e.errors = a.errors());
            return e
          };
          c = n(2);
          k.Syntax = c.Syntax;
          k.version =
            "3.1.3"
        }, function(c, k, n) {
          var l = n(2);
          c = function() {
            function a() {
              this.attach = !1;
              this.comments = [];
              this.stack = [];
              this.leading = [];
              this.trailing = []
            }
            a.prototype.insertInnerComments = function(a, h) {
              if (a.type === l.Syntax.BlockStatement && 0 === a.body.length) {
                for (var m = [], e = this.leading.length - 1; 0 <= e; --e) {
                  var g = this.leading[e];
                  h.end.offset >= g.start && (m.unshift(g.comment), this.leading.splice(e, 1), this.trailing.splice(e, 1))
                }
                m.length && (a.innerComments = m)
              }
            };
            a.prototype.findTrailingComments = function(a, h) {
              var m = [];
              if (0 <
                this.trailing.length) {
                for (var e = this.trailing.length - 1; 0 <= e; --e) {
                  var g = this.trailing[e];
                  g.start >= h.end.offset && m.unshift(g.comment)
                }
                this.trailing.length = 0;
                return m
              }(e = this.stack[this.stack.length - 1]) && e.node.trailingComments && (g = e.node.trailingComments[0]) && g.range[0] >= h.end.offset && (m = e.node.trailingComments, delete e.node.trailingComments);
              return m
            };
            a.prototype.findLeadingComments = function(a, h) {
              for (var m = [], e; 0 < this.stack.length;) {
                var g = this.stack[this.stack.length - 1];
                if (g && g.start >= h.start.offset) e =
                  this.stack.pop().node;
                else break
              }
              if (e) {
                for (var f = (e.leadingComments ? e.leadingComments.length : 0) - 1; 0 <= f; --f) g = e.leadingComments[f], g.range[1] <= h.start.offset && (m.unshift(g), e.leadingComments.splice(f, 1));
                e.leadingComments && 0 === e.leadingComments.length && delete e.leadingComments;
                return m
              }
              for (f = this.leading.length - 1; 0 <= f; --f) g = this.leading[f], g.start <= h.start.offset && (m.unshift(g.comment), this.leading.splice(f, 1));
              return m
            };
            a.prototype.visitNode = function(a, h) {
              if (!(a.type === l.Syntax.Program && 0 < a.body.length)) {
                this.insertInnerComments(a,
                  h);
                var m = this.findTrailingComments(a, h),
                  e = this.findLeadingComments(a, h);
                0 < e.length && (a.leadingComments = e);
                0 < m.length && (a.trailingComments = m);
                this.stack.push({
                  node: a,
                  start: h.start.offset
                })
              }
            };
            a.prototype.visitComment = function(a, h) {
              var c = "L" === a.type[0] ? "Line" : "Block",
                e = {
                  type: c,
                  value: a.value
                };
              a.range && (e.range = a.range);
              a.loc && (e.loc = a.loc);
              this.comments.push(e);
              this.attach && (e = {
                  comment: {
                    type: c,
                    value: a.value,
                    range: [h.start.offset, h.end.offset]
                  },
                  start: h.start.offset
                }, a.loc && (e.comment.loc = a.loc), a.type =
                c, this.leading.push(e), this.trailing.push(e))
            };
            a.prototype.visit = function(a, h) {
              "LineComment" === a.type ? this.visitComment(a, h) : "BlockComment" === a.type ? this.visitComment(a, h) : this.attach && this.visitNode(a, h)
            };
            return a
          }();
          k.CommentHandler = c
        }, function(c, k) {
          k.Syntax = {
            AssignmentExpression: "AssignmentExpression",
            AssignmentPattern: "AssignmentPattern",
            ArrayExpression: "ArrayExpression",
            ArrayPattern: "ArrayPattern",
            ArrowFunctionExpression: "ArrowFunctionExpression",
            BlockStatement: "BlockStatement",
            BinaryExpression: "BinaryExpression",
            BreakStatement: "BreakStatement",
            CallExpression: "CallExpression",
            CatchClause: "CatchClause",
            ClassBody: "ClassBody",
            ClassDeclaration: "ClassDeclaration",
            ClassExpression: "ClassExpression",
            ConditionalExpression: "ConditionalExpression",
            ContinueStatement: "ContinueStatement",
            DoWhileStatement: "DoWhileStatement",
            DebuggerStatement: "DebuggerStatement",
            EmptyStatement: "EmptyStatement",
            ExportAllDeclaration: "ExportAllDeclaration",
            ExportDefaultDeclaration: "ExportDefaultDeclaration",
            ExportNamedDeclaration: "ExportNamedDeclaration",
            ExportSpecifier: "ExportSpecifier",
            ExpressionStatement: "ExpressionStatement",
            ForStatement: "ForStatement",
            ForOfStatement: "ForOfStatement",
            ForInStatement: "ForInStatement",
            FunctionDeclaration: "FunctionDeclaration",
            FunctionExpression: "FunctionExpression",
            Identifier: "Identifier",
            IfStatement: "IfStatement",
            ImportDeclaration: "ImportDeclaration",
            ImportDefaultSpecifier: "ImportDefaultSpecifier",
            ImportNamespaceSpecifier: "ImportNamespaceSpecifier",
            ImportSpecifier: "ImportSpecifier",
            Literal: "Literal",
            LabeledStatement: "LabeledStatement",
            LogicalExpression: "LogicalExpression",
            MemberExpression: "MemberExpression",
            MetaProperty: "MetaProperty",
            MethodDefinition: "MethodDefinition",
            NewExpression: "NewExpression",
            ObjectExpression: "ObjectExpression",
            ObjectPattern: "ObjectPattern",
            Program: "Program",
            Property: "Property",
            RestElement: "RestElement",
            ReturnStatement: "ReturnStatement",
            SequenceExpression: "SequenceExpression",
            SpreadElement: "SpreadElement",
            Super: "Super",
            SwitchCase: "SwitchCase",
            SwitchStatement: "SwitchStatement",
            TaggedTemplateExpression: "TaggedTemplateExpression",
            TemplateElement: "TemplateElement",
            TemplateLiteral: "TemplateLiteral",
            ThisExpression: "ThisExpression",
            ThrowStatement: "ThrowStatement",
            TryStatement: "TryStatement",
            UnaryExpression: "UnaryExpression",
            UpdateExpression: "UpdateExpression",
            VariableDeclaration: "VariableDeclaration",
            VariableDeclarator: "VariableDeclarator",
            WhileStatement: "WhileStatement",
            WithStatement: "WithStatement",
            YieldExpression: "YieldExpression"
          }
        }, function(c, k, n) {
          var l = n(4),
            a = n(5),
            m = n(6),
            h = n(7),
            q = n(8),
            e = n(2),
            g = n(10);
          c = function() {
            function f(b,
              d, a) {
              void 0 === d && (d = {});
              this.config = {
                range: "boolean" === typeof d.range && d.range,
                loc: "boolean" === typeof d.loc && d.loc,
                source: null,
                tokens: "boolean" === typeof d.tokens && d.tokens,
                comment: "boolean" === typeof d.comment && d.comment,
                tolerant: "boolean" === typeof d.tolerant && d.tolerant
              };
              this.config.loc && d.source && null !== d.source && (this.config.source = String(d.source));
              this.delegate = a;
              this.errorHandler = new m.ErrorHandler;
              this.errorHandler.tolerant = this.config.tolerant;
              this.scanner = new q.Scanner(b, this.errorHandler);
              this.scanner.trackComment = this.config.comment;
              this.operatorPrecedence = {
                ")": 0,
                ";": 0,
                ",": 0,
                "=": 0,
                "]": 0,
                "||": 1,
                "&&": 2,
                "|": 3,
                "^": 4,
                "&": 5,
                "==": 6,
                "!=": 6,
                "===": 6,
                "!==": 6,
                "<": 7,
                ">": 7,
                "<=": 7,
                ">=": 7,
                "<<": 8,
                ">>": 8,
                ">>>": 8,
                "+": 9,
                "-": 9,
                "*": 11,
                "/": 11,
                "%": 11
              };
              this.sourceType = d && "module" === d.sourceType ? "module" : "script";
              this.lookahead = null;
              this.hasLineTerminator = !1;
              this.context = {
                allowIn: !0,
                allowYield: !0,
                firstCoverInitializedNameError: null,
                isAssignmentTarget: !1,
                isBindingElement: !1,
                inFunctionBody: !1,
                inIteration: !1,
                inSwitch: !1,
                labelSet: {},
                strict: "module" === this.sourceType
              };
              this.tokens = [];
              this.startMarker = {
                index: 0,
                lineNumber: this.scanner.lineNumber,
                lineStart: 0
              };
              this.lastMarker = {
                index: 0,
                lineNumber: this.scanner.lineNumber,
                lineStart: 0
              };
              this.nextToken();
              this.lastMarker = {
                index: this.scanner.index,
                lineNumber: this.scanner.lineNumber,
                lineStart: this.scanner.lineStart
              }
            }
            f.prototype.throwError = function(b) {
              for (var d = 1; d < arguments.length; d++);
              var a = Array.prototype.slice.call(arguments, 1);
              d = b.replace(/%(\d)/g, function(b, d) {
                l.assert(d <
                  a.length, "Message reference must be in range");
                return a[d]
              });
              throw this.errorHandler.createError(this.lastMarker.index, this.lastMarker.lineNumber, this.lastMarker.index - this.lastMarker.lineStart + 1, d);
            };
            f.prototype.tolerateError = function(b) {
              for (var d = 1; d < arguments.length; d++);
              var a = Array.prototype.slice.call(arguments, 1);
              d = b.replace(/%(\d)/g, function(b, d) {
                l.assert(d < a.length, "Message reference must be in range");
                return a[d]
              });
              this.errorHandler.tolerateError(this.lastMarker.index, this.scanner.lineNumber,
                this.lastMarker.index - this.lastMarker.lineStart + 1, d)
            };
            f.prototype.unexpectedTokenError = function(b, d) {
              var t = d || a.Messages.UnexpectedToken;
              if (b) {
                d || (t = b.type === h.Token.EOF ? a.Messages.UnexpectedEOS : b.type === h.Token.Identifier ? a.Messages.UnexpectedIdentifier : b.type === h.Token.NumericLiteral ? a.Messages.UnexpectedNumber : b.type === h.Token.StringLiteral ? a.Messages.UnexpectedString : b.type === h.Token.Template ? a.Messages.UnexpectedTemplate : a.Messages.UnexpectedToken, b.type === h.Token.Keyword && (this.scanner.isFutureReservedWord(b.value) ?
                  t = a.Messages.UnexpectedReserved : this.context.strict && this.scanner.isStrictModeReservedWord(b.value) && (t = a.Messages.StrictReservedWord)));
                var e = b.type === h.Token.Template ? b.value.raw : b.value
              } else e = "ILLEGAL";
              t = t.replace("%0", e);
              if (b && "number" === typeof b.lineNumber) {
                e = b.start;
                var g = b.lineNumber,
                  f = b.start - this.lastMarker.lineStart + 1
              } else e = this.lastMarker.index, g = this.lastMarker.lineNumber, f = e - this.lastMarker.lineStart + 1;
              return this.errorHandler.createError(e, g, f, t)
            };
            f.prototype.throwUnexpectedToken =
              function(b, d) {
                throw this.unexpectedTokenError(b, d);
              };
            f.prototype.tolerateUnexpectedToken = function(b, d) {
              this.errorHandler.tolerate(this.unexpectedTokenError(b, d))
            };
            f.prototype.collectComments = function() {
              if (this.config.comment) {
                var b = this.scanner.scanComments();
                if (0 < b.length && this.delegate)
                  for (var d = 0; d < b.length; ++d) {
                    var a = b[d];
                    var e = {
                      type: a.multiLine ? "BlockComment" : "LineComment",
                      value: this.scanner.source.slice(a.slice[0], a.slice[1])
                    };
                    this.config.range && (e.range = a.range);
                    this.config.loc && (e.loc = a.loc);
                    this.delegate(e, {
                      start: {
                        line: a.loc.start.line,
                        column: a.loc.start.column,
                        offset: a.range[0]
                      },
                      end: {
                        line: a.loc.end.line,
                        column: a.loc.end.column,
                        offset: a.range[1]
                      }
                    })
                  }
              } else this.scanner.scanComments()
            };
            f.prototype.getTokenRaw = function(b) {
              return this.scanner.source.slice(b.start, b.end)
            };
            f.prototype.convertToken = function(b) {
              var d = {
                type: h.TokenName[b.type],
                value: this.getTokenRaw(b)
              };
              this.config.range && (d.range = [b.start, b.end]);
              this.config.loc && (d.loc = {
                start: {
                  line: this.startMarker.lineNumber,
                  column: this.startMarker.index -
                    this.startMarker.lineStart
                },
                end: {
                  line: this.scanner.lineNumber,
                  column: this.scanner.index - this.scanner.lineStart
                }
              });
              b.regex && (d.regex = b.regex);
              return d
            };
            f.prototype.nextToken = function() {
              var b = this.lookahead;
              this.lastMarker.index = this.scanner.index;
              this.lastMarker.lineNumber = this.scanner.lineNumber;
              this.lastMarker.lineStart = this.scanner.lineStart;
              this.collectComments();
              this.startMarker.index = this.scanner.index;
              this.startMarker.lineNumber = this.scanner.lineNumber;
              this.startMarker.lineStart = this.scanner.lineStart;
              var d = this.scanner.lex();
              this.hasLineTerminator = b && d ? b.lineNumber !== d.lineNumber : !1;
              d && this.context.strict && d.type === h.Token.Identifier && this.scanner.isStrictModeReservedWord(d.value) && (d.type = h.Token.Keyword);
              this.lookahead = d;
              this.config.tokens && d.type !== h.Token.EOF && this.tokens.push(this.convertToken(d));
              return b
            };
            f.prototype.nextRegexToken = function() {
              this.collectComments();
              var b = this.scanner.scanRegExp();
              this.config.tokens && (this.tokens.pop(), this.tokens.push(this.convertToken(b)));
              this.lookahead =
                b;
              this.nextToken();
              return b
            };
            f.prototype.createNode = function() {
              return {
                index: this.startMarker.index,
                line: this.startMarker.lineNumber,
                column: this.startMarker.index - this.startMarker.lineStart
              }
            };
            f.prototype.startNode = function(b) {
              return {
                index: b.start,
                line: b.lineNumber,
                column: b.start - b.lineStart
              }
            };
            f.prototype.finalize = function(b, d) {
              this.config.range && (d.range = [b.index, this.lastMarker.index]);
              this.config.loc && (d.loc = {
                start: {
                  line: b.line,
                  column: b.column
                },
                end: {
                  line: this.lastMarker.lineNumber,
                  column: this.lastMarker.index -
                    this.lastMarker.lineStart
                }
              }, this.config.source && (d.loc.source = this.config.source));
              this.delegate && this.delegate(d, {
                start: {
                  line: b.line,
                  column: b.column,
                  offset: b.index
                },
                end: {
                  line: this.lastMarker.lineNumber,
                  column: this.lastMarker.index - this.lastMarker.lineStart,
                  offset: this.lastMarker.index
                }
              });
              return d
            };
            f.prototype.expect = function(b) {
              var d = this.nextToken();
              d.type === h.Token.Punctuator && d.value === b || this.throwUnexpectedToken(d)
            };
            f.prototype.expectCommaSeparator = function() {
              if (this.config.tolerant) {
                var b =
                  this.lookahead;
                b.type === h.Token.Punctuator && "," === b.value ? this.nextToken() : b.type === h.Token.Punctuator && ";" === b.value ? (this.nextToken(), this.tolerateUnexpectedToken(b)) : this.tolerateUnexpectedToken(b, a.Messages.UnexpectedToken)
              } else this.expect(",")
            };
            f.prototype.expectKeyword = function(b) {
              var d = this.nextToken();
              d.type === h.Token.Keyword && d.value === b || this.throwUnexpectedToken(d)
            };
            f.prototype.match = function(b) {
              return this.lookahead.type === h.Token.Punctuator && this.lookahead.value === b
            };
            f.prototype.matchKeyword =
              function(b) {
                return this.lookahead.type === h.Token.Keyword && this.lookahead.value === b
              };
            f.prototype.matchContextualKeyword = function(b) {
              return this.lookahead.type === h.Token.Identifier && this.lookahead.value === b
            };
            f.prototype.matchAssign = function() {
              if (this.lookahead.type !== h.Token.Punctuator) return !1;
              var b = this.lookahead.value;
              return "=" === b || "*=" === b || "**=" === b || "/=" === b || "%=" === b || "+=" === b || "-=" === b || "<<=" === b || ">>=" === b || ">>>=" === b || "&=" === b || "^=" === b || "|=" === b
            };
            f.prototype.isolateCoverGrammar = function(b) {
              var d =
                this.context.isBindingElement,
                a = this.context.isAssignmentTarget,
                e = this.context.firstCoverInitializedNameError;
              this.context.isBindingElement = !0;
              this.context.isAssignmentTarget = !0;
              this.context.firstCoverInitializedNameError = null;
              b = b.call(this);
              null !== this.context.firstCoverInitializedNameError && this.throwUnexpectedToken(this.context.firstCoverInitializedNameError);
              this.context.isBindingElement = d;
              this.context.isAssignmentTarget = a;
              this.context.firstCoverInitializedNameError = e;
              return b
            };
            f.prototype.inheritCoverGrammar =
              function(b) {
                var d = this.context.isBindingElement,
                  a = this.context.isAssignmentTarget,
                  e = this.context.firstCoverInitializedNameError;
                this.context.isBindingElement = !0;
                this.context.isAssignmentTarget = !0;
                this.context.firstCoverInitializedNameError = null;
                b = b.call(this);
                this.context.isBindingElement = this.context.isBindingElement && d;
                this.context.isAssignmentTarget = this.context.isAssignmentTarget && a;
                this.context.firstCoverInitializedNameError = e || this.context.firstCoverInitializedNameError;
                return b
              };
            f.prototype.consumeSemicolon =
              function() {
                this.match(";") ? this.nextToken() : this.hasLineTerminator || (this.lookahead.type === h.Token.EOF || this.match("}") || this.throwUnexpectedToken(this.lookahead), this.lastMarker.index = this.startMarker.index, this.lastMarker.lineNumber = this.startMarker.lineNumber, this.lastMarker.lineStart = this.startMarker.lineStart)
              };
            f.prototype.parsePrimaryExpression = function() {
              var b = this.createNode();
              switch (this.lookahead.type) {
                case h.Token.Identifier:
                  "module" === this.sourceType && "await" === this.lookahead.value && this.tolerateUnexpectedToken(this.lookahead);
                  var d = this.finalize(b, new g.Identifier(this.nextToken().value));
                  break;
                case h.Token.NumericLiteral:
                case h.Token.StringLiteral:
                  this.context.strict && this.lookahead.octal && this.tolerateUnexpectedToken(this.lookahead, a.Messages.StrictOctalLiteral);
                  this.context.isAssignmentTarget = !1;
                  this.context.isBindingElement = !1;
                  d = this.nextToken();
                  var e = this.getTokenRaw(d);
                  d = this.finalize(b, new g.Literal(d.value, e));
                  break;
                case h.Token.BooleanLiteral:
                  this.context.isAssignmentTarget = !1;
                  this.context.isBindingElement = !1;
                  d = this.nextToken();
                  d.value = "true" === d.value;
                  e = this.getTokenRaw(d);
                  d = this.finalize(b, new g.Literal(d.value, e));
                  break;
                case h.Token.NullLiteral:
                  this.context.isAssignmentTarget = !1;
                  this.context.isBindingElement = !1;
                  d = this.nextToken();
                  d.value = null;
                  e = this.getTokenRaw(d);
                  d = this.finalize(b, new g.Literal(d.value, e));
                  break;
                case h.Token.Template:
                  d = this.parseTemplateLiteral();
                  break;
                case h.Token.Punctuator:
                  e = this.lookahead.value;
                  switch (e) {
                    case "(":
                      this.context.isBindingElement = !1;
                      d = this.inheritCoverGrammar(this.parseGroupExpression);
                      break;
                    case "[":
                      d = this.inheritCoverGrammar(this.parseArrayInitializer);
                      break;
                    case "{":
                      d = this.inheritCoverGrammar(this.parseObjectInitializer);
                      break;
                    case "/":
                    case "/=":
                      this.context.isAssignmentTarget = !1;
                      this.context.isBindingElement = !1;
                      this.scanner.index = this.startMarker.index;
                      d = this.nextRegexToken();
                      e = this.getTokenRaw(d);
                      d = this.finalize(b, new g.RegexLiteral(d.value, e, d.regex));
                      break;
                    default:
                      this.throwUnexpectedToken(this.nextToken())
                  }
                  break;
                case h.Token.Keyword:
                  !this.context.strict && this.context.allowYield &&
                    this.matchKeyword("yield") ? d = this.parseIdentifierName() : !this.context.strict && this.matchKeyword("let") ? d = this.finalize(b, new g.Identifier(this.nextToken().value)) : (this.context.isAssignmentTarget = !1, this.context.isBindingElement = !1, this.matchKeyword("function") ? d = this.parseFunctionExpression() : this.matchKeyword("this") ? (this.nextToken(), d = this.finalize(b, new g.ThisExpression)) : this.matchKeyword("class") ? d = this.parseClassExpression() : this.throwUnexpectedToken(this.nextToken()));
                  break;
                default:
                  this.throwUnexpectedToken(this.nextToken())
              }
              return d
            };
            f.prototype.parseSpreadElement = function() {
              var b = this.createNode();
              this.expect("...");
              var d = this.inheritCoverGrammar(this.parseAssignmentExpression);
              return this.finalize(b, new g.SpreadElement(d))
            };
            f.prototype.parseArrayInitializer = function() {
              var b = this.createNode(),
                d = [];
              for (this.expect("["); !this.match("]");)
                if (this.match(",")) this.nextToken(), d.push(null);
                else if (this.match("...")) {
                var a = this.parseSpreadElement();
                this.match("]") || (this.context.isAssignmentTarget = !1, this.context.isBindingElement = !1,
                  this.expect(","));
                d.push(a)
              } else d.push(this.inheritCoverGrammar(this.parseAssignmentExpression)), this.match("]") || this.expect(",");
              this.expect("]");
              return this.finalize(b, new g.ArrayExpression(d))
            };
            f.prototype.parsePropertyMethod = function(b) {
              this.context.isAssignmentTarget = !1;
              this.context.isBindingElement = !1;
              var d = this.context.strict,
                a = this.isolateCoverGrammar(this.parseFunctionSourceElements);
              this.context.strict && b.firstRestricted && this.tolerateUnexpectedToken(b.firstRestricted, b.message);
              this.context.strict &&
                b.stricted && this.tolerateUnexpectedToken(b.stricted, b.message);
              this.context.strict = d;
              return a
            };
            f.prototype.parsePropertyMethodFunction = function() {
              var b = this.createNode(),
                d = this.context.allowYield;
              this.context.allowYield = !1;
              var a = this.parseFormalParameters(),
                e = this.parsePropertyMethod(a);
              this.context.allowYield = d;
              return this.finalize(b, new g.FunctionExpression(null, a.params, e, !1))
            };
            f.prototype.parseObjectPropertyKey = function() {
              var b = this.createNode(),
                d = this.nextToken(),
                e = null;
              switch (d.type) {
                case h.Token.StringLiteral:
                case h.Token.NumericLiteral:
                  this.context.strict &&
                    d.octal && this.tolerateUnexpectedToken(d, a.Messages.StrictOctalLiteral);
                  e = this.getTokenRaw(d);
                  e = this.finalize(b, new g.Literal(d.value, e));
                  break;
                case h.Token.Identifier:
                case h.Token.BooleanLiteral:
                case h.Token.NullLiteral:
                case h.Token.Keyword:
                  e = this.finalize(b, new g.Identifier(d.value));
                  break;
                case h.Token.Punctuator:
                  "[" === d.value ? (e = this.isolateCoverGrammar(this.parseAssignmentExpression), this.expect("]")) : this.throwUnexpectedToken(d);
                  break;
                default:
                  this.throwUnexpectedToken(d)
              }
              return e
            };
            f.prototype.isPropertyKey =
              function(b, d) {
                return b.type === e.Syntax.Identifier && b.name === d || b.type === e.Syntax.Literal && b.value === d
              };
            f.prototype.parseObjectProperty = function(b) {
              var d = this.createNode(),
                e = this.lookahead,
                p = !1,
                f = !1,
                c = !1;
              if (e.type === h.Token.Identifier) {
                this.nextToken();
                var m = this.finalize(d, new g.Identifier(e.value))
              } else this.match("*") ? this.nextToken() : (p = this.match("["), m = this.parseObjectPropertyKey());
              var k = this.qualifiedPropertyName(this.lookahead);
              if (e.type === h.Token.Identifier && "get" === e.value && k) {
                k = "get";
                p =
                  this.match("[");
                m = this.parseObjectPropertyKey();
                this.context.allowYield = !1;
                var l = this.parseGetterMethod()
              } else e.type === h.Token.Identifier && "set" === e.value && k ? (k = "set", p = this.match("["), m = this.parseObjectPropertyKey(), l = this.parseSetterMethod()) : e.type === h.Token.Punctuator && "*" === e.value && k ? (k = "init", p = this.match("["), m = this.parseObjectPropertyKey(), l = this.parseGeneratorMethod(), f = !0) : (m || this.throwUnexpectedToken(this.lookahead), k = "init", this.match(":") ? (!p && this.isPropertyKey(m, "__proto__") && (b.value &&
                this.tolerateError(a.Messages.DuplicateProtoProperty), b.value = !0), this.nextToken(), l = this.inheritCoverGrammar(this.parseAssignmentExpression)) : this.match("(") ? (l = this.parsePropertyMethodFunction(), f = !0) : e.type === h.Token.Identifier ? (b = this.finalize(d, new g.Identifier(e.value)), this.match("=") ? (this.context.firstCoverInitializedNameError = this.lookahead, this.nextToken(), c = !0, e = this.isolateCoverGrammar(this.parseAssignmentExpression), l = this.finalize(d, new g.AssignmentPattern(b, e))) : (c = !0, l = b)) : this.throwUnexpectedToken(this.nextToken()));
              return this.finalize(d, new g.Property(k, m, p, l, f, c))
            };
            f.prototype.parseObjectInitializer = function() {
              var b = this.createNode();
              this.expect("{");
              for (var d = [], a = {
                  value: !1
                }; !this.match("}");) d.push(this.parseObjectProperty(a)), this.match("}") || this.expectCommaSeparator();
              this.expect("}");
              return this.finalize(b, new g.ObjectExpression(d))
            };
            f.prototype.parseTemplateHead = function() {
              l.assert(this.lookahead.head, "Template literal must start with a template head");
              var b = this.createNode(),
                d = this.nextToken();
              return this.finalize(b,
                new g.TemplateElement({
                  raw: d.value.raw,
                  cooked: d.value.cooked
                }, d.tail))
            };
            f.prototype.parseTemplateElement = function() {
              this.lookahead.type !== h.Token.Template && this.throwUnexpectedToken();
              var b = this.createNode(),
                d = this.nextToken();
              return this.finalize(b, new g.TemplateElement({
                raw: d.value.raw,
                cooked: d.value.cooked
              }, d.tail))
            };
            f.prototype.parseTemplateLiteral = function() {
              var b = this.createNode(),
                d = [],
                a = [],
                e = this.parseTemplateHead();
              for (a.push(e); !e.tail;) d.push(this.parseExpression()), e = this.parseTemplateElement(),
                a.push(e);
              return this.finalize(b, new g.TemplateLiteral(a, d))
            };
            f.prototype.reinterpretExpressionAsPattern = function(b) {
              switch (b.type) {
                case e.Syntax.SpreadElement:
                  b.type = e.Syntax.RestElement;
                  this.reinterpretExpressionAsPattern(b.argument);
                  break;
                case e.Syntax.ArrayExpression:
                  b.type = e.Syntax.ArrayPattern;
                  for (var d = 0; d < b.elements.length; d++) null !== b.elements[d] && this.reinterpretExpressionAsPattern(b.elements[d]);
                  break;
                case e.Syntax.ObjectExpression:
                  b.type = e.Syntax.ObjectPattern;
                  for (d = 0; d < b.properties.length; d++) this.reinterpretExpressionAsPattern(b.properties[d].value);
                  break;
                case e.Syntax.AssignmentExpression:
                  b.type = e.Syntax.AssignmentPattern, delete b.operator, this.reinterpretExpressionAsPattern(b.left)
              }
            };
            f.prototype.parseGroupExpression = function() {
              this.expect("(");
              if (this.match(")")) {
                this.nextToken();
                this.match("=>") || this.expect("=>");
                var b = {
                  type: "ArrowParameterPlaceHolder",
                  params: []
                }
              } else {
                var d = this.lookahead,
                  a = [];
                if (this.match("...")) b = this.parseRestElement(a), this.expect(")"), this.match("=>") || this.expect("=>"), b = {
                  type: "ArrowParameterPlaceHolder",
                  params: [b]
                };
                else {
                  var p = !1;
                  this.context.isBindingElement = !0;
                  b = this.inheritCoverGrammar(this.parseAssignmentExpression);
                  if (this.match(",")) {
                    var f = [];
                    this.context.isAssignmentTarget = !1;
                    for (f.push(b); this.startMarker.index < this.scanner.length && this.match(",");) {
                      this.nextToken();
                      if (this.match("...")) {
                        this.context.isBindingElement || this.throwUnexpectedToken(this.lookahead);
                        f.push(this.parseRestElement(a));
                        this.expect(")");
                        this.match("=>") || this.expect("=>");
                        this.context.isBindingElement = !1;
                        for (p = 0; p < f.length; p++) this.reinterpretExpressionAsPattern(f[p]);
                        p = !0;
                        b = {
                          type: "ArrowParameterPlaceHolder",
                          params: f
                        }
                      } else f.push(this.inheritCoverGrammar(this.parseAssignmentExpression));
                      if (p) break
                    }
                    p || (b = this.finalize(this.startNode(d), new g.SequenceExpression(f)))
                  }
                  if (!p) {
                    this.expect(")");
                    if (this.match("=>") && (b.type === e.Syntax.Identifier && "yield" === b.name && (p = !0, b = {
                        type: "ArrowParameterPlaceHolder",
                        params: [b]
                      }), !p)) {
                      this.context.isBindingElement || this.throwUnexpectedToken(this.lookahead);
                      if (b.type === e.Syntax.SequenceExpression)
                        for (p = 0; p < b.expressions.length; p++) this.reinterpretExpressionAsPattern(b.expressions[p]);
                      else this.reinterpretExpressionAsPattern(b);
                      b = {
                        type: "ArrowParameterPlaceHolder",
                        params: b.type === e.Syntax.SequenceExpression ? b.expressions : [b]
                      }
                    }
                    this.context.isBindingElement = !1
                  }
                }
              }
              return b
            };
            f.prototype.parseArguments = function() {
              this.expect("(");
              var b = [];
              if (!this.match(")"))
                for (;;) {
                  var d = this.match("...") ? this.parseSpreadElement() : this.isolateCoverGrammar(this.parseAssignmentExpression);
                  b.push(d);
                  if (this.match(")")) break;
                  this.expectCommaSeparator()
                }
              this.expect(")");
              return b
            };
            f.prototype.isIdentifierName =
              function(b) {
                return b.type === h.Token.Identifier || b.type === h.Token.Keyword || b.type === h.Token.BooleanLiteral || b.type === h.Token.NullLiteral
              };
            f.prototype.parseIdentifierName = function() {
              var b = this.createNode(),
                d = this.nextToken();
              this.isIdentifierName(d) || this.throwUnexpectedToken(d);
              return this.finalize(b, new g.Identifier(d.value))
            };
            f.prototype.parseNewExpression = function() {
              var b = this.createNode(),
                d = this.parseIdentifierName();
              l.assert("new" === d.name, "New expression must start with `new`");
              if (this.match("."))
                if (this.nextToken(),
                  this.lookahead.type === h.Token.Identifier && this.context.inFunctionBody && "target" === this.lookahead.value) {
                  var a = this.parseIdentifierName();
                  a = new g.MetaProperty(d, a)
                } else this.throwUnexpectedToken(this.lookahead);
              else d = this.isolateCoverGrammar(this.parseLeftHandSideExpression), a = this.match("(") ? this.parseArguments() : [], a = new g.NewExpression(d, a), this.context.isAssignmentTarget = !1, this.context.isBindingElement = !1;
              return this.finalize(b, a)
            };
            f.prototype.parseLeftHandSideExpressionAllowCall = function() {
              var b =
                this.lookahead,
                d = this.context.allowIn;
              this.context.allowIn = !0;
              if (this.matchKeyword("super") && this.context.inFunctionBody) {
                var a = this.createNode();
                this.nextToken();
                a = this.finalize(a, new g.Super);
                this.match("(") || this.match(".") || this.match("[") || this.throwUnexpectedToken(this.lookahead)
              } else a = this.inheritCoverGrammar(this.matchKeyword("new") ? this.parseNewExpression : this.parsePrimaryExpression);
              for (;;)
                if (this.match(".")) {
                  this.context.isBindingElement = !1;
                  this.context.isAssignmentTarget = !0;
                  this.expect(".");
                  var e = this.parseIdentifierName();
                  a = this.finalize(this.startNode(b), new g.StaticMemberExpression(a, e))
                } else if (this.match("(")) this.context.isBindingElement = !1, this.context.isAssignmentTarget = !1, e = this.parseArguments(), a = this.finalize(this.startNode(b), new g.CallExpression(a, e));
              else if (this.match("[")) this.context.isBindingElement = !1, this.context.isAssignmentTarget = !0, this.expect("["), e = this.isolateCoverGrammar(this.parseExpression), this.expect("]"), a = this.finalize(this.startNode(b), new g.ComputedMemberExpression(a,
                e));
              else if (this.lookahead.type === h.Token.Template && this.lookahead.head) e = this.parseTemplateLiteral(), a = this.finalize(this.startNode(b), new g.TaggedTemplateExpression(a, e));
              else break;
              this.context.allowIn = d;
              return a
            };
            f.prototype.parseSuper = function() {
              var b = this.createNode();
              this.expectKeyword("super");
              this.match("[") || this.match(".") || this.throwUnexpectedToken(this.lookahead);
              return this.finalize(b, new g.Super)
            };
            f.prototype.parseLeftHandSideExpression = function() {
              l.assert(this.context.allowIn, "callee of new expression always allow in keyword.");
              for (var b = this.startNode(this.lookahead), d = this.matchKeyword("super") && this.context.inFunctionBody ? this.parseSuper() : this.inheritCoverGrammar(this.matchKeyword("new") ? this.parseNewExpression : this.parsePrimaryExpression);;)
                if (this.match("[")) {
                  this.context.isBindingElement = !1;
                  this.context.isAssignmentTarget = !0;
                  this.expect("[");
                  var a = this.isolateCoverGrammar(this.parseExpression);
                  this.expect("]");
                  d = this.finalize(b, new g.ComputedMemberExpression(d, a))
                } else if (this.match(".")) this.context.isBindingElement = !1, this.context.isAssignmentTarget = !0, this.expect("."), a = this.parseIdentifierName(), d = this.finalize(b, new g.StaticMemberExpression(d, a));
              else if (this.lookahead.type === h.Token.Template && this.lookahead.head) a = this.parseTemplateLiteral(), d = this.finalize(b, new g.TaggedTemplateExpression(d, a));
              else break;
              return d
            };
            f.prototype.parseUpdateExpression = function() {
              var b = this.lookahead;
              if (this.match("++") || this.match("--")) {
                b = this.startNode(b);
                var d = this.nextToken();
                var f = this.inheritCoverGrammar(this.parseUnaryExpression);
                this.context.strict && f.type === e.Syntax.Identifier && this.scanner.isRestrictedWord(f.name) && this.tolerateError(a.Messages.StrictLHSPrefix);
                this.context.isAssignmentTarget || this.tolerateError(a.Messages.InvalidLHSInAssignment);
                f = this.finalize(b, new g.UpdateExpression(d.value, f, !0));
                this.context.isAssignmentTarget = !1;
                this.context.isBindingElement = !1
              } else f = this.inheritCoverGrammar(this.parseLeftHandSideExpressionAllowCall), this.hasLineTerminator || this.lookahead.type !== h.Token.Punctuator || !this.match("++") &&
                !this.match("--") || (this.context.strict && f.type === e.Syntax.Identifier && this.scanner.isRestrictedWord(f.name) && this.tolerateError(a.Messages.StrictLHSPostfix), this.context.isAssignmentTarget || this.tolerateError(a.Messages.InvalidLHSInAssignment), this.context.isAssignmentTarget = !1, this.context.isBindingElement = !1, d = this.nextToken().value, f = this.finalize(this.startNode(b), new g.UpdateExpression(d, f, !1)));
              return f
            };
            f.prototype.parseUnaryExpression = function() {
              if (this.match("+") || this.match("-") || this.match("~") ||
                this.match("!") || this.matchKeyword("delete") || this.matchKeyword("void") || this.matchKeyword("typeof")) {
                var b = this.startNode(this.lookahead),
                  d = this.nextToken();
                var f = this.inheritCoverGrammar(this.parseUnaryExpression);
                f = this.finalize(b, new g.UnaryExpression(d.value, f));
                this.context.strict && "delete" === f.operator && f.argument.type === e.Syntax.Identifier && this.tolerateError(a.Messages.StrictDelete);
                this.context.isAssignmentTarget = !1;
                this.context.isBindingElement = !1
              } else f = this.parseUpdateExpression();
              return f
            };
            f.prototype.parseExponentiationExpression = function() {
              var b = this.lookahead,
                d = this.inheritCoverGrammar(this.parseUnaryExpression);
              if (d.type !== e.Syntax.UnaryExpression && this.match("**")) {
                this.nextToken();
                this.context.isAssignmentTarget = !1;
                this.context.isBindingElement = !1;
                var a = this.isolateCoverGrammar(this.parseExponentiationExpression);
                d = this.finalize(this.startNode(b), new g.BinaryExpression("**", d, a))
              }
              return d
            };
            f.prototype.binaryPrecedence = function(b) {
              var d = b.value;
              return b.type === h.Token.Punctuator ?
                this.operatorPrecedence[d] || 0 : b.type === h.Token.Keyword ? "instanceof" === d || this.context.allowIn && "in" === d ? 7 : 0 : 0
            };
            f.prototype.parseBinaryExpression = function() {
              var b = this.lookahead,
                d = this.inheritCoverGrammar(this.parseExponentiationExpression),
                a = this.lookahead,
                e = this.binaryPrecedence(a);
              if (0 < e) {
                this.nextToken();
                a.prec = e;
                this.context.isAssignmentTarget = !1;
                this.context.isBindingElement = !1;
                b = [b, this.lookahead];
                for (var f = this.isolateCoverGrammar(this.parseExponentiationExpression), h = [d, a, f];;) {
                  e = this.binaryPrecedence(this.lookahead);
                  if (0 >= e) break;
                  for (; 2 < h.length && e <= h[h.length - 2].prec;) {
                    f = h.pop();
                    var c = h.pop().value;
                    d = h.pop();
                    b.pop();
                    a = this.startNode(b[b.length - 1]);
                    h.push(this.finalize(a, new g.BinaryExpression(c, d, f)))
                  }
                  a = this.nextToken();
                  a.prec = e;
                  h.push(a);
                  b.push(this.lookahead);
                  h.push(this.isolateCoverGrammar(this.parseExponentiationExpression))
                }
                e = h.length - 1;
                d = h[e];
                for (b.pop(); 1 < e;) a = this.startNode(b.pop()), d = this.finalize(a, new g.BinaryExpression(h[e - 1].value, h[e - 2], d)), e -= 2
              }
              return d
            };
            f.prototype.parseConditionalExpression =
              function() {
                var b = this.lookahead,
                  d = this.inheritCoverGrammar(this.parseBinaryExpression);
                if (this.match("?")) {
                  this.nextToken();
                  var a = this.context.allowIn;
                  this.context.allowIn = !0;
                  var e = this.isolateCoverGrammar(this.parseAssignmentExpression);
                  this.context.allowIn = a;
                  this.expect(":");
                  a = this.isolateCoverGrammar(this.parseAssignmentExpression);
                  d = this.finalize(this.startNode(b), new g.ConditionalExpression(d, e, a));
                  this.context.isAssignmentTarget = !1;
                  this.context.isBindingElement = !1
                }
                return d
              };
            f.prototype.checkPatternParam =
              function(b, d) {
                switch (d.type) {
                  case e.Syntax.Identifier:
                    this.validateParam(b, d, d.name);
                    break;
                  case e.Syntax.RestElement:
                    this.checkPatternParam(b, d.argument);
                    break;
                  case e.Syntax.AssignmentPattern:
                    this.checkPatternParam(b, d.left);
                    break;
                  case e.Syntax.ArrayPattern:
                    for (var a = 0; a < d.elements.length; a++) null !== d.elements[a] && this.checkPatternParam(b, d.elements[a]);
                    break;
                  case e.Syntax.YieldExpression:
                    break;
                  default:
                    for (l.assert(d.type === e.Syntax.ObjectPattern, "Invalid type"), a = 0; a < d.properties.length; a++) this.checkPatternParam(b,
                      d.properties[a].value)
                }
              };
            f.prototype.reinterpretAsCoverFormalsList = function(b) {
              var d = [b];
              switch (b.type) {
                case e.Syntax.Identifier:
                  break;
                case "ArrowParameterPlaceHolder":
                  d = b.params;
                  break;
                default:
                  return null
              }
              b = {
                paramSet: {}
              };
              for (var g = 0; g < d.length; ++g) {
                var f = d[g];
                f.type === e.Syntax.AssignmentPattern && f.right.type === e.Syntax.YieldExpression && (f.right.argument && this.throwUnexpectedToken(this.lookahead), f.right.type = e.Syntax.Identifier, f.right.name = "yield", delete f.right.argument, delete f.right.delegate);
                this.checkPatternParam(b, f);
                d[g] = f
              }
              if (this.context.strict || !this.context.allowYield)
                for (g = 0; g < d.length; ++g) f = d[g], f.type === e.Syntax.YieldExpression && this.throwUnexpectedToken(this.lookahead);
              b.message === a.Messages.StrictParamDupe && this.throwUnexpectedToken(this.context.strict ? b.stricted : b.firstRestricted, b.message);
              return {
                params: d,
                stricted: b.stricted,
                firstRestricted: b.firstRestricted,
                message: b.message
              }
            };
            f.prototype.parseAssignmentExpression = function() {
              if (!this.context.allowYield && this.matchKeyword("yield")) var b =
                this.parseYieldExpression();
              else {
                var d = this.lookahead,
                  f = d;
                b = this.parseConditionalExpression();
                if ("ArrowParameterPlaceHolder" === b.type || this.match("=>")) {
                  if (this.context.isAssignmentTarget = !1, this.context.isBindingElement = !1, f = this.reinterpretAsCoverFormalsList(b)) {
                    this.hasLineTerminator && this.tolerateUnexpectedToken(this.lookahead);
                    this.context.firstCoverInitializedNameError = null;
                    var p = this.context.strict,
                      h = this.context.allowYield;
                    this.context.allowYield = !0;
                    b = this.startNode(d);
                    this.expect("=>");
                    d =
                      this.match("{") ? this.parseFunctionSourceElements() : this.isolateCoverGrammar(this.parseAssignmentExpression);
                    var c = d.type !== e.Syntax.BlockStatement;
                    this.context.strict && f.firstRestricted && this.throwUnexpectedToken(f.firstRestricted, f.message);
                    this.context.strict && f.stricted && this.tolerateUnexpectedToken(f.stricted, f.message);
                    b = this.finalize(b, new g.ArrowFunctionExpression(f.params, d, c));
                    this.context.strict = p;
                    this.context.allowYield = h
                  }
                } else this.matchAssign() && (this.context.isAssignmentTarget || this.tolerateError(a.Messages.InvalidLHSInAssignment),
                  this.context.strict && b.type === e.Syntax.Identifier && (p = b, this.scanner.isRestrictedWord(p.name) && this.tolerateUnexpectedToken(f, a.Messages.StrictLHSAssignment), this.scanner.isStrictModeReservedWord(p.name) && this.tolerateUnexpectedToken(f, a.Messages.StrictReservedWord)), this.match("=") ? this.reinterpretExpressionAsPattern(b) : (this.context.isAssignmentTarget = !1, this.context.isBindingElement = !1), f = this.nextToken(), p = this.isolateCoverGrammar(this.parseAssignmentExpression), b = this.finalize(this.startNode(d),
                    new g.AssignmentExpression(f.value, b, p)), this.context.firstCoverInitializedNameError = null)
              }
              return b
            };
            f.prototype.parseExpression = function() {
              var b = this.lookahead,
                d = this.isolateCoverGrammar(this.parseAssignmentExpression);
              if (this.match(",")) {
                var a = [];
                for (a.push(d); this.startMarker.index < this.scanner.length && this.match(",");) this.nextToken(), a.push(this.isolateCoverGrammar(this.parseAssignmentExpression));
                d = this.finalize(this.startNode(b), new g.SequenceExpression(a))
              }
              return d
            };
            f.prototype.parseStatementListItem =
              function() {
                this.context.isAssignmentTarget = !0;
                this.context.isBindingElement = !0;
                if (this.lookahead.type === h.Token.Keyword) switch (this.lookahead.value) {
                  case "export":
                    "module" !== this.sourceType && this.tolerateUnexpectedToken(this.lookahead, a.Messages.IllegalExportDeclaration);
                    var b = this.parseExportDeclaration();
                    break;
                  case "import":
                    "module" !== this.sourceType && this.tolerateUnexpectedToken(this.lookahead, a.Messages.IllegalImportDeclaration);
                    b = this.parseImportDeclaration();
                    break;
                  case "const":
                    b = this.parseLexicalDeclaration({
                      inFor: !1
                    });
                    break;
                  case "function":
                    b = this.parseFunctionDeclaration();
                    break;
                  case "class":
                    b = this.parseClassDeclaration();
                    break;
                  case "let":
                    b = this.isLexicalDeclaration() ? this.parseLexicalDeclaration({
                      inFor: !1
                    }) : this.parseStatement();
                    break;
                  default:
                    b = this.parseStatement()
                } else b = this.parseStatement();
                return b
              };
            f.prototype.parseBlock = function() {
              var b = this.createNode();
              this.expect("{");
              for (var d = []; !this.match("}");) d.push(this.parseStatementListItem());
              this.expect("}");
              return this.finalize(b, new g.BlockStatement(d))
            };
            f.prototype.parseLexicalBinding = function(b, d) {
              var f = this.createNode(),
                p = this.parsePattern([], b);
              this.context.strict && p.type === e.Syntax.Identifier && this.scanner.isRestrictedWord(p.name) && this.tolerateError(a.Messages.StrictVarName);
              var h = null;
              if ("const" === b) this.matchKeyword("in") || this.matchContextualKeyword("of") || (this.expect("="), h = this.isolateCoverGrammar(this.parseAssignmentExpression));
              else if (!d.inFor && p.type !== e.Syntax.Identifier || this.match("=")) this.expect("="), h = this.isolateCoverGrammar(this.parseAssignmentExpression);
              return this.finalize(f, new g.VariableDeclarator(p, h))
            };
            f.prototype.parseBindingList = function(b, d) {
              for (var a = [this.parseLexicalBinding(b, d)]; this.match(",");) this.nextToken(), a.push(this.parseLexicalBinding(b, d));
              return a
            };
            f.prototype.isLexicalDeclaration = function() {
              var b = this.scanner.index,
                d = this.scanner.lineNumber,
                a = this.scanner.lineStart;
              this.collectComments();
              var e = this.scanner.lex();
              this.scanner.index = b;
              this.scanner.lineNumber = d;
              this.scanner.lineStart = a;
              return e.type === h.Token.Identifier || e.type ===
                h.Token.Punctuator && "[" === e.value || e.type === h.Token.Punctuator && "{" === e.value || e.type === h.Token.Keyword && "let" === e.value || e.type === h.Token.Keyword && "yield" === e.value
            };
            f.prototype.parseLexicalDeclaration = function(b) {
              var d = this.createNode(),
                a = this.nextToken().value;
              l.assert("let" === a || "const" === a, "Lexical declaration must be either let or const");
              b = this.parseBindingList(a, b);
              this.consumeSemicolon();
              return this.finalize(d, new g.VariableDeclaration(b, a))
            };
            f.prototype.parseBindingRestElement = function(b,
              d) {
              var a = this.createNode();
              this.expect("...");
              var e = this.parsePattern(b, d);
              return this.finalize(a, new g.RestElement(e))
            };
            f.prototype.parseArrayPattern = function(b, d) {
              var a = this.createNode();
              this.expect("[");
              for (var e = []; !this.match("]");)
                if (this.match(",")) this.nextToken(), e.push(null);
                else {
                  if (this.match("...")) {
                    e.push(this.parseBindingRestElement(b, d));
                    break
                  } else e.push(this.parsePatternWithDefault(b, d));
                  this.match("]") || this.expect(",")
                }
              this.expect("]");
              return this.finalize(a, new g.ArrayPattern(e))
            };
            f.prototype.parsePropertyPattern = function(b, d) {
              var a = this.createNode(),
                e = !1,
                f = !1;
              if (this.lookahead.type === h.Token.Identifier) {
                var c = this.lookahead;
                var m = this.parseVariableIdentifier();
                var k = this.finalize(a, new g.Identifier(c.value));
                if (this.match("=")) {
                  b.push(c);
                  f = !0;
                  this.nextToken();
                  var l = this.parseAssignmentExpression();
                  c = this.finalize(this.startNode(c), new g.AssignmentPattern(k, l))
                } else this.match(":") ? (this.expect(":"), c = this.parsePatternWithDefault(b, d)) : (b.push(c), f = !0, c = k)
              } else e = this.match("["),
                m = this.parseObjectPropertyKey(), this.expect(":"), c = this.parsePatternWithDefault(b, d);
              return this.finalize(a, new g.Property("init", m, e, c, !1, f))
            };
            f.prototype.parseObjectPattern = function(b, d) {
              var a = this.createNode(),
                e = [];
              for (this.expect("{"); !this.match("}");) e.push(this.parsePropertyPattern(b, d)), this.match("}") || this.expect(",");
              this.expect("}");
              return this.finalize(a, new g.ObjectPattern(e))
            };
            f.prototype.parsePattern = function(b, d) {
              if (this.match("[")) var e = this.parseArrayPattern(b, d);
              else this.match("{") ?
                e = this.parseObjectPattern(b, d) : (!this.matchKeyword("let") || "const" !== d && "let" !== d || this.tolerateUnexpectedToken(this.lookahead, a.Messages.UnexpectedToken), b.push(this.lookahead), e = this.parseVariableIdentifier(d));
              return e
            };
            f.prototype.parsePatternWithDefault = function(b, d) {
              var a = this.lookahead,
                e = this.parsePattern(b, d);
              if (this.match("=")) {
                this.nextToken();
                var f = this.context.allowYield;
                this.context.allowYield = !0;
                var h = this.isolateCoverGrammar(this.parseAssignmentExpression);
                this.context.allowYield = f;
                e = this.finalize(this.startNode(a), new g.AssignmentPattern(e, h))
              }
              return e
            };
            f.prototype.parseVariableIdentifier = function(b) {
              var d = this.createNode(),
                e = this.nextToken();
              e.type === h.Token.Keyword && "yield" === e.value ? (this.context.strict && this.tolerateUnexpectedToken(e, a.Messages.StrictReservedWord), this.context.allowYield || this.throwUnexpectedToken(e)) : e.type !== h.Token.Identifier ? this.context.strict && e.type === h.Token.Keyword && this.scanner.isStrictModeReservedWord(e.value) ? this.tolerateUnexpectedToken(e,
                a.Messages.StrictReservedWord) : (this.context.strict || "let" !== e.value || "var" !== b) && this.throwUnexpectedToken(e) : "module" === this.sourceType && e.type === h.Token.Identifier && "await" === e.value && this.tolerateUnexpectedToken(e);
              return this.finalize(d, new g.Identifier(e.value))
            };
            f.prototype.parseVariableDeclaration = function(b) {
              var d = this.createNode(),
                f = this.parsePattern([], "var");
              this.context.strict && f.type === e.Syntax.Identifier && this.scanner.isRestrictedWord(f.name) && this.tolerateError(a.Messages.StrictVarName);
              var h = null;
              this.match("=") ? (this.nextToken(), h = this.isolateCoverGrammar(this.parseAssignmentExpression)) : f.type === e.Syntax.Identifier || b.inFor || this.expect("=");
              return this.finalize(d, new g.VariableDeclarator(f, h))
            };
            f.prototype.parseVariableDeclarationList = function(b) {
              b = {
                inFor: b.inFor
              };
              var d = [];
              for (d.push(this.parseVariableDeclaration(b)); this.match(",");) this.nextToken(), d.push(this.parseVariableDeclaration(b));
              return d
            };
            f.prototype.parseVariableStatement = function() {
              var b = this.createNode();
              this.expectKeyword("var");
              var d = this.parseVariableDeclarationList({
                inFor: !1
              });
              this.consumeSemicolon();
              return this.finalize(b, new g.VariableDeclaration(d, "var"))
            };
            f.prototype.parseEmptyStatement = function() {
              var b = this.createNode();
              this.expect(";");
              return this.finalize(b, new g.EmptyStatement)
            };
            f.prototype.parseExpressionStatement = function() {
              var b = this.createNode(),
                d = this.parseExpression();
              this.consumeSemicolon();
              return this.finalize(b, new g.ExpressionStatement(d))
            };
            f.prototype.parseIfStatement = function() {
              var b = this.createNode(),
                d = null;
              this.expectKeyword("if");
              this.expect("(");
              var a = this.parseExpression();
              if (!this.match(")") && this.config.tolerant) {
                this.tolerateUnexpectedToken(this.nextToken());
                var e = this.finalize(this.createNode(), new g.EmptyStatement)
              } else this.expect(")"), e = this.parseStatement(), this.matchKeyword("else") && (this.nextToken(), d = this.parseStatement());
              return this.finalize(b, new g.IfStatement(a, e, d))
            };
            f.prototype.parseDoWhileStatement = function() {
              var b = this.createNode();
              this.expectKeyword("do");
              var d = this.context.inIteration;
              this.context.inIteration = !0;
              var a = this.parseStatement();
              this.context.inIteration = d;
              this.expectKeyword("while");
              this.expect("(");
              d = this.parseExpression();
              this.expect(")");
              this.match(";") && this.nextToken();
              return this.finalize(b, new g.DoWhileStatement(a, d))
            };
            f.prototype.parseWhileStatement = function() {
              var b = this.createNode();
              this.expectKeyword("while");
              this.expect("(");
              var d = this.parseExpression();
              if (!this.match(")") && this.config.tolerant) {
                this.tolerateUnexpectedToken(this.nextToken());
                var a = this.finalize(this.createNode(),
                  new g.EmptyStatement)
              } else {
                this.expect(")");
                var e = this.context.inIteration;
                this.context.inIteration = !0;
                a = this.parseStatement();
                this.context.inIteration = e
              }
              return this.finalize(b, new g.WhileStatement(d, a))
            };
            f.prototype.parseForStatement = function() {
              var b = null,
                d = null,
                f = null,
                h = !0,
                c = this.createNode();
              this.expectKeyword("for");
              this.expect("(");
              if (this.match(";")) this.nextToken();
              else if (this.matchKeyword("var")) {
                b = this.createNode();
                this.nextToken();
                var m = this.context.allowIn;
                this.context.allowIn = !1;
                var k =
                  this.parseVariableDeclarationList({
                    inFor: !0
                  });
                this.context.allowIn = m;
                if (1 === k.length && this.matchKeyword("in")) {
                  var l = k[0];
                  l.init && (l.id.type === e.Syntax.ArrayPattern || l.id.type === e.Syntax.ObjectPattern || this.context.strict) && this.tolerateError(a.Messages.ForInOfLoopInitializer, "for-in");
                  b = this.finalize(b, new g.VariableDeclaration(k, "var"));
                  this.nextToken();
                  l = b;
                  var n = this.parseExpression();
                  b = null
                } else 1 === k.length && null === k[0].init && this.matchContextualKeyword("of") ? (b = this.finalize(b, new g.VariableDeclaration(k,
                  "var")), this.nextToken(), l = b, n = this.parseAssignmentExpression(), b = null, h = !1) : (b = this.finalize(b, new g.VariableDeclaration(k, "var")), this.expect(";"))
              } else if (this.matchKeyword("const") || this.matchKeyword("let")) {
                b = this.createNode();
                var q = this.nextToken().value;
                this.context.strict || "in" !== this.lookahead.value ? (m = this.context.allowIn, this.context.allowIn = !1, k = this.parseBindingList(q, {
                  inFor: !0
                }), this.context.allowIn = m, 1 === k.length && null === k[0].init && this.matchKeyword("in") ? (b = this.finalize(b, new g.VariableDeclaration(k,
                  q)), this.nextToken(), l = b, n = this.parseExpression(), b = null) : 1 === k.length && null === k[0].init && this.matchContextualKeyword("of") ? (b = this.finalize(b, new g.VariableDeclaration(k, q)), this.nextToken(), l = b, n = this.parseAssignmentExpression(), b = null, h = !1) : (this.consumeSemicolon(), b = this.finalize(b, new g.VariableDeclaration(k, q)))) : (b = this.finalize(b, new g.Identifier(q)), this.nextToken(), l = b, n = this.parseExpression(), b = null)
              } else if (k = this.lookahead, m = this.context.allowIn, this.context.allowIn = !1, b = this.inheritCoverGrammar(this.parseAssignmentExpression),
                this.context.allowIn = m, this.matchKeyword("in")) this.context.isAssignmentTarget && b.type !== e.Syntax.AssignmentExpression || this.tolerateError(a.Messages.InvalidLHSInForIn), this.nextToken(), this.reinterpretExpressionAsPattern(b), l = b, n = this.parseExpression(), b = null;
              else if (this.matchContextualKeyword("of")) this.context.isAssignmentTarget && b.type !== e.Syntax.AssignmentExpression || this.tolerateError(a.Messages.InvalidLHSInForLoop), this.nextToken(), this.reinterpretExpressionAsPattern(b), l = b, n = this.parseAssignmentExpression(),
                b = null, h = !1;
              else {
                if (this.match(",")) {
                  for (b = [b]; this.match(",");) this.nextToken(), b.push(this.isolateCoverGrammar(this.parseAssignmentExpression));
                  b = this.finalize(this.startNode(k), new g.SequenceExpression(b))
                }
                this.expect(";")
              }
              "undefined" === typeof l && (this.match(";") || (d = this.parseExpression()), this.expect(";"), this.match(")") || (f = this.parseExpression()));
              !this.match(")") && this.config.tolerant ? (this.tolerateUnexpectedToken(this.nextToken()), m = this.finalize(this.createNode(), new g.EmptyStatement)) :
                (this.expect(")"), k = this.context.inIteration, this.context.inIteration = !0, m = this.isolateCoverGrammar(this.parseStatement), this.context.inIteration = k);
              return "undefined" === typeof l ? this.finalize(c, new g.ForStatement(b, d, f, m)) : h ? this.finalize(c, new g.ForInStatement(l, n, m)) : this.finalize(c, new g.ForOfStatement(l, n, m))
            };
            f.prototype.parseContinueStatement = function() {
              var b = this.createNode();
              this.expectKeyword("continue");
              var d = null;
              this.lookahead.type !== h.Token.Identifier || this.hasLineTerminator || (d = this.parseVariableIdentifier(),
                Object.prototype.hasOwnProperty.call(this.context.labelSet, "$" + d.name) || this.throwError(a.Messages.UnknownLabel, d.name));
              this.consumeSemicolon();
              null !== d || this.context.inIteration || this.throwError(a.Messages.IllegalContinue);
              return this.finalize(b, new g.ContinueStatement(d))
            };
            f.prototype.parseBreakStatement = function() {
              var b = this.createNode();
              this.expectKeyword("break");
              var d = null;
              this.lookahead.type !== h.Token.Identifier || this.hasLineTerminator || (d = this.parseVariableIdentifier(), Object.prototype.hasOwnProperty.call(this.context.labelSet,
                "$" + d.name) || this.throwError(a.Messages.UnknownLabel, d.name));
              this.consumeSemicolon();
              null !== d || this.context.inIteration || this.context.inSwitch || this.throwError(a.Messages.IllegalBreak);
              return this.finalize(b, new g.BreakStatement(d))
            };
            f.prototype.parseReturnStatement = function() {
              this.context.inFunctionBody || this.tolerateError(a.Messages.IllegalReturn);
              var b = this.createNode();
              this.expectKeyword("return");
              var d = this.match(";") || this.match("}") || this.hasLineTerminator || this.lookahead.type === h.Token.EOF ?
                null : this.parseExpression();
              this.consumeSemicolon();
              return this.finalize(b, new g.ReturnStatement(d))
            };
            f.prototype.parseWithStatement = function() {
              this.context.strict && this.tolerateError(a.Messages.StrictModeWith);
              var b = this.createNode();
              this.expectKeyword("with");
              this.expect("(");
              var d = this.parseExpression();
              this.expect(")");
              var e = this.parseStatement();
              return this.finalize(b, new g.WithStatement(d, e))
            };
            f.prototype.parseSwitchCase = function() {
              var b = this.createNode();
              if (this.matchKeyword("default")) {
                this.nextToken();
                var d = null
              } else this.expectKeyword("case"), d = this.parseExpression();
              this.expect(":");
              for (var a = []; !(this.match("}") || this.matchKeyword("default") || this.matchKeyword("case"));) a.push(this.parseStatementListItem());
              return this.finalize(b, new g.SwitchCase(d, a))
            };
            f.prototype.parseSwitchStatement = function() {
              var b = this.createNode();
              this.expectKeyword("switch");
              this.expect("(");
              var d = this.parseExpression();
              this.expect(")");
              var e = this.context.inSwitch;
              this.context.inSwitch = !0;
              var f = [],
                h = !1;
              for (this.expect("{"); !this.match("}");) {
                var c =
                  this.parseSwitchCase();
                null === c.test && (h && this.throwError(a.Messages.MultipleDefaultsInSwitch), h = !0);
                f.push(c)
              }
              this.expect("}");
              this.context.inSwitch = e;
              return this.finalize(b, new g.SwitchStatement(d, f))
            };
            f.prototype.parseLabelledStatement = function() {
              var b = this.createNode(),
                d = this.parseExpression();
              if (d.type === e.Syntax.Identifier && this.match(":")) {
                this.nextToken();
                var f = "$" + d.name;
                Object.prototype.hasOwnProperty.call(this.context.labelSet, f) && this.throwError(a.Messages.Redeclaration, "Label", d.name);
                this.context.labelSet[f] = !0;
                var h = this.parseStatement();
                delete this.context.labelSet[f];
                d = new g.LabeledStatement(d, h)
              } else this.consumeSemicolon(), d = new g.ExpressionStatement(d);
              return this.finalize(b, d)
            };
            f.prototype.parseThrowStatement = function() {
              var b = this.createNode();
              this.expectKeyword("throw");
              this.hasLineTerminator && this.throwError(a.Messages.NewlineAfterThrow);
              var d = this.parseExpression();
              this.consumeSemicolon();
              return this.finalize(b, new g.ThrowStatement(d))
            };
            f.prototype.parseCatchClause =
              function() {
                var b = this.createNode();
                this.expectKeyword("catch");
                this.expect("(");
                this.match(")") && this.throwUnexpectedToken(this.lookahead);
                for (var d = [], f = this.parsePattern(d), h = {}, c = 0; c < d.length; c++) {
                  var m = "$" + d[c].value;
                  Object.prototype.hasOwnProperty.call(h, m) && this.tolerateError(a.Messages.DuplicateBinding, d[c].value);
                  h[m] = !0
                }
                this.context.strict && f.type === e.Syntax.Identifier && this.scanner.isRestrictedWord(f.name) && this.tolerateError(a.Messages.StrictCatchVariable);
                this.expect(")");
                d = this.parseBlock();
                return this.finalize(b, new g.CatchClause(f, d))
              };
            f.prototype.parseFinallyClause = function() {
              this.expectKeyword("finally");
              return this.parseBlock()
            };
            f.prototype.parseTryStatement = function() {
              var b = this.createNode();
              this.expectKeyword("try");
              var d = this.parseBlock(),
                e = this.matchKeyword("catch") ? this.parseCatchClause() : null,
                f = this.matchKeyword("finally") ? this.parseFinallyClause() : null;
              e || f || this.throwError(a.Messages.NoCatchOrFinally);
              return this.finalize(b, new g.TryStatement(d, e, f))
            };
            f.prototype.parseDebuggerStatement =
              function() {
                var b = this.createNode();
                this.expectKeyword("debugger");
                this.consumeSemicolon();
                return this.finalize(b, new g.DebuggerStatement)
              };
            f.prototype.parseStatement = function() {
              var b = null;
              switch (this.lookahead.type) {
                case h.Token.BooleanLiteral:
                case h.Token.NullLiteral:
                case h.Token.NumericLiteral:
                case h.Token.StringLiteral:
                case h.Token.Template:
                case h.Token.RegularExpression:
                  b = this.parseExpressionStatement();
                  break;
                case h.Token.Punctuator:
                  b = this.lookahead.value;
                  b = "{" === b ? this.parseBlock() : "(" === b ? this.parseExpressionStatement() :
                    ";" === b ? this.parseEmptyStatement() : this.parseExpressionStatement();
                  break;
                case h.Token.Identifier:
                  b = this.parseLabelledStatement();
                  break;
                case h.Token.Keyword:
                  switch (this.lookahead.value) {
                    case "break":
                      b = this.parseBreakStatement();
                      break;
                    case "continue":
                      b = this.parseContinueStatement();
                      break;
                    case "debugger":
                      b = this.parseDebuggerStatement();
                      break;
                    case "do":
                      b = this.parseDoWhileStatement();
                      break;
                    case "for":
                      b = this.parseForStatement();
                      break;
                    case "function":
                      b = this.parseFunctionDeclaration();
                      break;
                    case "if":
                      b = this.parseIfStatement();
                      break;
                    case "return":
                      b = this.parseReturnStatement();
                      break;
                    case "switch":
                      b = this.parseSwitchStatement();
                      break;
                    case "throw":
                      b = this.parseThrowStatement();
                      break;
                    case "try":
                      b = this.parseTryStatement();
                      break;
                    case "var":
                      b = this.parseVariableStatement();
                      break;
                    case "while":
                      b = this.parseWhileStatement();
                      break;
                    case "with":
                      b = this.parseWithStatement();
                      break;
                    default:
                      b = this.parseExpressionStatement()
                  }
                  break;
                default:
                  this.throwUnexpectedToken(this.lookahead)
              }
              return b
            };
            f.prototype.parseFunctionSourceElements = function() {
              var b =
                this.createNode();
              this.expect("{");
              var d = this.parseDirectivePrologues(),
                a = this.context.labelSet,
                e = this.context.inIteration,
                f = this.context.inSwitch,
                h = this.context.inFunctionBody;
              this.context.labelSet = {};
              this.context.inIteration = !1;
              this.context.inSwitch = !1;
              for (this.context.inFunctionBody = !0; this.startMarker.index < this.scanner.length && !this.match("}");) d.push(this.parseStatementListItem());
              this.expect("}");
              this.context.labelSet = a;
              this.context.inIteration = e;
              this.context.inSwitch = f;
              this.context.inFunctionBody =
                h;
              return this.finalize(b, new g.BlockStatement(d))
            };
            f.prototype.validateParam = function(b, d, e) {
              var f = "$" + e;
              this.context.strict ? (this.scanner.isRestrictedWord(e) && (b.stricted = d, b.message = a.Messages.StrictParamName), Object.prototype.hasOwnProperty.call(b.paramSet, f) && (b.stricted = d, b.message = a.Messages.StrictParamDupe)) : b.firstRestricted || (this.scanner.isRestrictedWord(e) ? (b.firstRestricted = d, b.message = a.Messages.StrictParamName) : this.scanner.isStrictModeReservedWord(e) ? (b.firstRestricted = d, b.message =
                a.Messages.StrictReservedWord) : Object.prototype.hasOwnProperty.call(b.paramSet, f) && (b.stricted = d, b.message = a.Messages.StrictParamDupe));
              "function" === typeof Object.defineProperty ? Object.defineProperty(b.paramSet, f, {
                value: !0,
                enumerable: !0,
                writable: !0,
                configurable: !0
              }) : b.paramSet[f] = !0
            };
            f.prototype.parseRestElement = function(b) {
              var d = this.createNode();
              this.expect("...");
              b = this.parsePattern(b);
              this.match("=") && this.throwError(a.Messages.DefaultRestParameter);
              this.match(")") || this.throwError(a.Messages.ParameterAfterRestParameter);
              return this.finalize(d, new g.RestElement(b))
            };
            f.prototype.parseFormalParameter = function(b) {
              for (var d = [], a = this.match("...") ? this.parseRestElement(d) : this.parsePatternWithDefault(d), e = 0; e < d.length; e++) this.validateParam(b, d[e], d[e].value);
              b.params.push(a);
              return !this.match(")")
            };
            f.prototype.parseFormalParameters = function(b) {
              b = {
                params: [],
                firstRestricted: b
              };
              this.expect("(");
              if (!this.match(")"))
                for (b.paramSet = {}; this.startMarker.index < this.scanner.length && this.parseFormalParameter(b);) this.expect(",");
              this.expect(")");
              return {
                params: b.params,
                stricted: b.stricted,
                firstRestricted: b.firstRestricted,
                message: b.message
              }
            };
            f.prototype.parseFunctionDeclaration = function(b) {
              var d = this.createNode();
              this.expectKeyword("function");
              var e = this.match("*");
              e && this.nextToken();
              var f = null,
                h = null;
              if (!b || !this.match("("))
                if (b = this.lookahead, f = this.parseVariableIdentifier(), this.context.strict) this.scanner.isRestrictedWord(b.value) && this.tolerateUnexpectedToken(b, a.Messages.StrictFunctionName);
                else if (this.scanner.isRestrictedWord(b.value)) {
                h =
                  b;
                var c = a.Messages.StrictFunctionName
              } else this.scanner.isStrictModeReservedWord(b.value) && (h = b, c = a.Messages.StrictReservedWord);
              b = this.context.allowYield;
              this.context.allowYield = !e;
              var m = this.parseFormalParameters(h),
                k = m.params,
                l = m.stricted;
              h = m.firstRestricted;
              m.message && (c = m.message);
              m = this.context.strict;
              var n = this.parseFunctionSourceElements();
              this.context.strict && h && this.throwUnexpectedToken(h, c);
              this.context.strict && l && this.tolerateUnexpectedToken(l, c);
              this.context.strict = m;
              this.context.allowYield =
                b;
              return this.finalize(d, new g.FunctionDeclaration(f, k, n, e))
            };
            f.prototype.parseFunctionExpression = function() {
              var b = this.createNode();
              this.expectKeyword("function");
              var d = this.match("*");
              d && this.nextToken();
              var e = null,
                f = this.context.allowYield;
              this.context.allowYield = !d;
              if (!this.match("(")) {
                var h = this.lookahead;
                e = this.context.strict || d || !this.matchKeyword("yield") ? this.parseVariableIdentifier() : this.parseIdentifierName();
                if (this.context.strict) this.scanner.isRestrictedWord(h.value) && this.tolerateUnexpectedToken(h,
                  a.Messages.StrictFunctionName);
                else if (this.scanner.isRestrictedWord(h.value)) {
                  var c = h;
                  var m = a.Messages.StrictFunctionName
                } else this.scanner.isStrictModeReservedWord(h.value) && (c = h, m = a.Messages.StrictReservedWord)
              }
              var k = this.parseFormalParameters(c);
              h = k.params;
              var l = k.stricted;
              c = k.firstRestricted;
              k.message && (m = k.message);
              k = this.context.strict;
              var n = this.parseFunctionSourceElements();
              this.context.strict && c && this.throwUnexpectedToken(c, m);
              this.context.strict && l && this.tolerateUnexpectedToken(l, m);
              this.context.strict =
                k;
              this.context.allowYield = f;
              return this.finalize(b, new g.FunctionExpression(e, h, n, d))
            };
            f.prototype.parseDirective = function() {
              var b = this.lookahead,
                d = null,
                a = this.createNode(),
                f = this.parseExpression();
              f.type === e.Syntax.Literal && (d = this.getTokenRaw(b).slice(1, -1));
              this.consumeSemicolon();
              return this.finalize(a, d ? new g.Directive(f, d) : new g.ExpressionStatement(f))
            };
            f.prototype.parseDirectivePrologues = function() {
              for (var b = null, d = [];;) {
                var e = this.lookahead;
                if (e.type !== h.Token.StringLiteral) break;
                var f = this.parseDirective();
                d.push(f);
                f = f.directive;
                if ("string" !== typeof f) break;
                "use strict" === f ? (this.context.strict = !0, b && this.tolerateUnexpectedToken(b, a.Messages.StrictOctalLiteral)) : !b && e.octal && (b = e)
              }
              return d
            };
            f.prototype.qualifiedPropertyName = function(b) {
              switch (b.type) {
                case h.Token.Identifier:
                case h.Token.StringLiteral:
                case h.Token.BooleanLiteral:
                case h.Token.NullLiteral:
                case h.Token.NumericLiteral:
                case h.Token.Keyword:
                  return !0;
                case h.Token.Punctuator:
                  return "[" === b.value
              }
              return !1
            };
            f.prototype.parseGetterMethod = function() {
              var b =
                this.createNode();
              this.expect("(");
              this.expect(")");
              var d = {
                  params: [],
                  stricted: null,
                  firstRestricted: null,
                  message: null
                },
                a = this.context.allowYield;
              this.context.allowYield = !1;
              var e = this.parsePropertyMethod(d);
              this.context.allowYield = a;
              return this.finalize(b, new g.FunctionExpression(null, d.params, e, !1))
            };
            f.prototype.parseSetterMethod = function() {
              var b = this.createNode(),
                d = {
                  params: [],
                  firstRestricted: null,
                  paramSet: {}
                },
                a = this.context.allowYield;
              this.context.allowYield = !1;
              this.expect("(");
              this.match(")") ? this.tolerateUnexpectedToken(this.lookahead) :
                this.parseFormalParameter(d);
              this.expect(")");
              var e = this.parsePropertyMethod(d);
              this.context.allowYield = a;
              return this.finalize(b, new g.FunctionExpression(null, d.params, e, !1))
            };
            f.prototype.parseGeneratorMethod = function() {
              var b = this.createNode(),
                a = this.context.allowYield;
              this.context.allowYield = !0;
              var e = this.parseFormalParameters();
              this.context.allowYield = !1;
              var f = this.parsePropertyMethod(e);
              this.context.allowYield = a;
              return this.finalize(b, new g.FunctionExpression(null, e.params, f, !0))
            };
            f.prototype.isStartOfExpression =
              function() {
                var b = !0,
                  a = this.lookahead.value;
                switch (this.lookahead.type) {
                  case h.Token.Punctuator:
                    b = "[" === a || "(" === a || "{" === a || "+" === a || "-" === a || "!" === a || "~" === a || "++" === a || "--" === a || "/" === a || "/=" === a;
                    break;
                  case h.Token.Keyword:
                    b = "class" === a || "delete" === a || "function" === a || "let" === a || "new" === a || "super" === a || "this" === a || "typeof" === a || "void" === a || "yield" === a
                }
                return b
              };
            f.prototype.parseYieldExpression = function() {
              var b = this.createNode();
              this.expectKeyword("yield");
              var a = null,
                e = !1;
              if (!this.hasLineTerminator) {
                var f =
                  this.context.allowYield;
                this.context.allowYield = !1;
                (e = this.match("*")) ? (this.nextToken(), a = this.parseAssignmentExpression()) : this.isStartOfExpression() && (a = this.parseAssignmentExpression());
                this.context.allowYield = f
              }
              return this.finalize(b, new g.YieldExpression(a, e))
            };
            f.prototype.parseClassElement = function(b) {
              var e = this.lookahead,
                f = this.createNode(),
                c = !1,
                m = !1,
                k = !1;
              if (this.match("*")) this.nextToken();
              else {
                c = this.match("[");
                var l = this.parseObjectPropertyKey();
                "static" === l.name && (this.qualifiedPropertyName(this.lookahead) ||
                  this.match("*")) && (e = this.lookahead, k = !0, c = this.match("["), this.match("*") ? this.nextToken() : l = this.parseObjectPropertyKey())
              }
              var n = this.qualifiedPropertyName(this.lookahead);
              if (e.type === h.Token.Identifier)
                if ("get" === e.value && n) {
                  var q = "get";
                  c = this.match("[");
                  l = this.parseObjectPropertyKey();
                  this.context.allowYield = !1;
                  var w = this.parseGetterMethod()
                } else "set" === e.value && n && (q = "set", c = this.match("["), l = this.parseObjectPropertyKey(), w = this.parseSetterMethod());
              else e.type === h.Token.Punctuator && "*" === e.value &&
                n && (q = "init", c = this.match("["), l = this.parseObjectPropertyKey(), w = this.parseGeneratorMethod(), m = !0);
              !q && l && this.match("(") && (q = "init", w = this.parsePropertyMethodFunction(), m = !0);
              q || this.throwUnexpectedToken(this.lookahead);
              "init" === q && (q = "method");
              c || (k && this.isPropertyKey(l, "prototype") && this.throwUnexpectedToken(e, a.Messages.StaticPrototype), !k && this.isPropertyKey(l, "constructor") && ("method" === q && m && !w.generator || this.throwUnexpectedToken(e, a.Messages.ConstructorSpecialMethod), b.value ? this.throwUnexpectedToken(e,
                a.Messages.DuplicateConstructor) : b.value = !0, q = "constructor"));
              return this.finalize(f, new g.MethodDefinition(l, c, w, q, k))
            };
            f.prototype.parseClassElementList = function() {
              var b = [],
                a = {
                  value: !1
                };
              for (this.expect("{"); !this.match("}");) this.match(";") ? this.nextToken() : b.push(this.parseClassElement(a));
              this.expect("}");
              return b
            };
            f.prototype.parseClassBody = function() {
              var b = this.createNode(),
                a = this.parseClassElementList();
              return this.finalize(b, new g.ClassBody(a))
            };
            f.prototype.parseClassDeclaration = function(b) {
              var a =
                this.createNode(),
                e = this.context.strict;
              this.context.strict = !0;
              this.expectKeyword("class");
              b = b && this.lookahead.type !== h.Token.Identifier ? null : this.parseVariableIdentifier();
              var f = null;
              this.matchKeyword("extends") && (this.nextToken(), f = this.isolateCoverGrammar(this.parseLeftHandSideExpressionAllowCall));
              var c = this.parseClassBody();
              this.context.strict = e;
              return this.finalize(a, new g.ClassDeclaration(b, f, c))
            };
            f.prototype.parseClassExpression = function() {
              var b = this.createNode(),
                a = this.context.strict;
              this.context.strict = !0;
              this.expectKeyword("class");
              var e = this.lookahead.type === h.Token.Identifier ? this.parseVariableIdentifier() : null,
                f = null;
              this.matchKeyword("extends") && (this.nextToken(), f = this.isolateCoverGrammar(this.parseLeftHandSideExpressionAllowCall));
              var c = this.parseClassBody();
              this.context.strict = a;
              return this.finalize(b, new g.ClassExpression(e, f, c))
            };
            f.prototype.parseProgram = function() {
              for (var b = this.createNode(), a = this.parseDirectivePrologues(); this.startMarker.index < this.scanner.length;) a.push(this.parseStatementListItem());
              return this.finalize(b, new g.Program(a, this.sourceType))
            };
            f.prototype.parseModuleSpecifier = function() {
              var b = this.createNode();
              this.lookahead.type !== h.Token.StringLiteral && this.throwError(a.Messages.InvalidModuleSpecifier);
              var e = this.nextToken(),
                f = this.getTokenRaw(e);
              return this.finalize(b, new g.Literal(e.value, f))
            };
            f.prototype.parseImportSpecifier = function() {
              var b = this.createNode(),
                a;
              if (this.lookahead.type === h.Token.Identifier) {
                var e = a = this.parseVariableIdentifier();
                this.matchContextualKeyword("as") &&
                  (this.nextToken(), e = this.parseVariableIdentifier())
              } else e = a = this.parseIdentifierName(), this.matchContextualKeyword("as") ? (this.nextToken(), e = this.parseVariableIdentifier()) : this.throwUnexpectedToken(this.nextToken());
              return this.finalize(b, new g.ImportSpecifier(e, a))
            };
            f.prototype.parseNamedImports = function() {
              this.expect("{");
              for (var b = []; !this.match("}");) b.push(this.parseImportSpecifier()), this.match("}") || this.expect(",");
              this.expect("}");
              return b
            };
            f.prototype.parseImportDefaultSpecifier = function() {
              var b =
                this.createNode(),
                a = this.parseIdentifierName();
              return this.finalize(b, new g.ImportDefaultSpecifier(a))
            };
            f.prototype.parseImportNamespaceSpecifier = function() {
              var b = this.createNode();
              this.expect("*");
              this.matchContextualKeyword("as") || this.throwError(a.Messages.NoAsAfterImportNamespace);
              this.nextToken();
              var e = this.parseIdentifierName();
              return this.finalize(b, new g.ImportNamespaceSpecifier(e))
            };
            f.prototype.parseImportDeclaration = function() {
              this.context.inFunctionBody && this.throwError(a.Messages.IllegalImportDeclaration);
              var b = this.createNode();
              this.expectKeyword("import");
              var e = [];
              this.lookahead.type !== h.Token.StringLiteral && (this.match("{") ? e = e.concat(this.parseNamedImports()) : this.match("*") ? e.push(this.parseImportNamespaceSpecifier()) : this.isIdentifierName(this.lookahead) && !this.matchKeyword("default") ? (e.push(this.parseImportDefaultSpecifier()), this.match(",") && (this.nextToken(), this.match("*") ? e.push(this.parseImportNamespaceSpecifier()) : this.match("{") ? e = e.concat(this.parseNamedImports()) : this.throwUnexpectedToken(this.lookahead))) :
                this.throwUnexpectedToken(this.nextToken()), this.matchContextualKeyword("from") || this.throwError(this.lookahead.value ? a.Messages.UnexpectedToken : a.Messages.MissingFromClause, this.lookahead.value), this.nextToken());
              var f = this.parseModuleSpecifier();
              this.consumeSemicolon();
              return this.finalize(b, new g.ImportDeclaration(e, f))
            };
            f.prototype.parseExportSpecifier = function() {
              var b = this.createNode(),
                a = this.parseIdentifierName(),
                e = a;
              this.matchContextualKeyword("as") && (this.nextToken(), e = this.parseIdentifierName());
              return this.finalize(b, new g.ExportSpecifier(a, e))
            };
            f.prototype.parseExportDeclaration = function() {
              this.context.inFunctionBody && this.throwError(a.Messages.IllegalExportDeclaration);
              var b = this.createNode();
              this.expectKeyword("export");
              if (this.matchKeyword("default")) {
                this.nextToken();
                if (this.matchKeyword("function")) var e = this.parseFunctionDeclaration(!0);
                else this.matchKeyword("class") ? e = this.parseClassDeclaration(!0) : (this.matchContextualKeyword("from") && this.throwError(a.Messages.UnexpectedToken,
                  this.lookahead.value), e = this.match("{") ? this.parseObjectInitializer() : this.match("[") ? this.parseArrayInitializer() : this.parseAssignmentExpression(), this.consumeSemicolon());
                b = this.finalize(b, new g.ExportDefaultDeclaration(e))
              } else if (this.match("*")) {
                this.nextToken();
                if (!this.matchContextualKeyword("from")) {
                  var f = this.lookahead.value ? a.Messages.UnexpectedToken : a.Messages.MissingFromClause;
                  this.throwError(f, this.lookahead.value)
                }
                this.nextToken();
                e = this.parseModuleSpecifier();
                this.consumeSemicolon();
                b = this.finalize(b, new g.ExportAllDeclaration(e))
              } else if (this.lookahead.type === h.Token.Keyword) {
                e = void 0;
                switch (this.lookahead.value) {
                  case "let":
                  case "const":
                    e = this.parseLexicalDeclaration({
                      inFor: !1
                    });
                    break;
                  case "var":
                  case "class":
                  case "function":
                    e = this.parseStatementListItem();
                    break;
                  default:
                    this.throwUnexpectedToken(this.lookahead)
                }
                b = this.finalize(b, new g.ExportNamedDeclaration(e, [], null))
              } else {
                e = [];
                var c = null;
                f = !1;
                for (this.expect("{"); !this.match("}");) f = f || this.matchKeyword("default"), e.push(this.parseExportSpecifier()),
                  this.match("}") || this.expect(",");
                this.expect("}");
                this.matchContextualKeyword("from") ? (this.nextToken(), c = this.parseModuleSpecifier(), this.consumeSemicolon()) : f ? (f = this.lookahead.value ? a.Messages.UnexpectedToken : a.Messages.MissingFromClause, this.throwError(f, this.lookahead.value)) : this.consumeSemicolon();
                b = this.finalize(b, new g.ExportNamedDeclaration(null, e, c))
              }
              return b
            };
            return f
          }();
          k.Parser = c
        }, function(c, k) {
          k.assert = function(c, k) {
            if (!c) throw Error("ASSERT: " + k);
          }
        }, function(c, k) {
          k.Messages = {
            UnexpectedToken: "Unexpected token %0",
            UnexpectedTokenIllegal: "Unexpected token ILLEGAL",
            UnexpectedNumber: "Unexpected number",
            UnexpectedString: "Unexpected string",
            UnexpectedIdentifier: "Unexpected identifier",
            UnexpectedReserved: "Unexpected reserved word",
            UnexpectedTemplate: "Unexpected quasi %0",
            UnexpectedEOS: "Unexpected end of input",
            NewlineAfterThrow: "Illegal newline after throw",
            InvalidRegExp: "Invalid regular expression",
            UnterminatedRegExp: "Invalid regular expression: missing /",
            InvalidLHSInAssignment: "Invalid left-hand side in assignment",
            InvalidLHSInForIn: "Invalid left-hand side in for-in",
            InvalidLHSInForLoop: "Invalid left-hand side in for-loop",
            MultipleDefaultsInSwitch: "More than one default clause in switch statement",
            NoCatchOrFinally: "Missing catch or finally after try",
            UnknownLabel: "Undefined label '%0'",
            Redeclaration: "%0 '%1' has already been declared",
            IllegalContinue: "Illegal continue statement",
            IllegalBreak: "Illegal break statement",
            IllegalReturn: "Illegal return statement",
            StrictModeWith: "Strict mode code may not include a with statement",
            StrictCatchVariable: "Catch variable may not be eval or arguments in strict mode",
            StrictVarName: "Variable name may not be eval or arguments in strict mode",
            StrictParamName: "Parameter name eval or arguments is not allowed in strict mode",
            StrictParamDupe: "Strict mode function may not have duplicate parameter names",
            StrictFunctionName: "Function name may not be eval or arguments in strict mode",
            StrictOctalLiteral: "Octal literals are not allowed in strict mode.",
            StrictDelete: "Delete of an unqualified identifier in strict mode.",
            StrictLHSAssignment: "Assignment to eval or arguments is not allowed in strict mode",
            StrictLHSPostfix: "Postfix increment/decrement may not have eval or arguments operand in strict mode",
            StrictLHSPrefix: "Prefix increment/decrement may not have eval or arguments operand in strict mode",
            StrictReservedWord: "Use of future reserved word in strict mode",
            TemplateOctalLiteral: "Octal literals are not allowed in template strings.",
            ParameterAfterRestParameter: "Rest parameter must be last formal parameter",
            DefaultRestParameter: "Unexpected token =",
            DuplicateProtoProperty: "Duplicate __proto__ fields are not allowed in object literals",
            ConstructorSpecialMethod: "Class constructor may not be an accessor",
            DuplicateConstructor: "A class may only have one constructor",
            StaticPrototype: "Classes may not have static property named prototype",
            MissingFromClause: "Unexpected token",
            NoAsAfterImportNamespace: "Unexpected token",
            InvalidModuleSpecifier: "Unexpected token",
            IllegalImportDeclaration: "Unexpected token",
            IllegalExportDeclaration: "Unexpected token",
            DuplicateBinding: "Duplicate binding %0",
            ForInOfLoopInitializer: "%0 loop variable declaration may not have an initializer"
          }
        }, function(c, k) {
          var n = function() {
            function c() {
              this.errors = [];
              this.tolerant = !1
            }
            c.prototype.recordError = function(a) {
              this.errors.push(a)
            };
            c.prototype.tolerate = function(a) {
              if (this.tolerant) this.recordError(a);
              else throw a;
            };
            c.prototype.constructError = function(a, c) {
              var h = Error(a);
              try {
                throw h;
              } catch (q) {
                Object.create && Object.defineProperty && (h = Object.create(q), Object.defineProperty(h, "column", {
                  value: c
                }))
              } finally {
                return h
              }
            };
            c.prototype.createError = function(a, c, h, k) {
              h = this.constructError("Line " + c + ": " + k, h);
              h.index = a;
              h.lineNumber = c;
              h.description = k;
              return h
            };
            c.prototype.throwError = function(a, c, h, k) {
              throw this.createError(a, c, h, k);
            };
            c.prototype.tolerateError = function(a, c, h, k) {
              a = this.createError(a, c, h, k);
              if (this.tolerant) this.recordError(a);
              else throw a;
            };
            return c
          }();
          k.ErrorHandler = n
        }, function(c, k) {
          var n = k.Token || (k.Token = {});
          n[n.BooleanLiteral = 1] = "BooleanLiteral";
          n[n.EOF = 2] = "EOF";
          n[n.Identifier = 3] = "Identifier";
          n[n.Keyword =
            4] = "Keyword";
          n[n.NullLiteral = 5] = "NullLiteral";
          n[n.NumericLiteral = 6] = "NumericLiteral";
          n[n.Punctuator = 7] = "Punctuator";
          n[n.StringLiteral = 8] = "StringLiteral";
          n[n.RegularExpression = 9] = "RegularExpression";
          n[n.Template = 10] = "Template";
          n = k.Token;
          k.TokenName = {};
          k.TokenName[n.BooleanLiteral] = "Boolean";
          k.TokenName[n.EOF] = "<end>";
          k.TokenName[n.Identifier] = "Identifier";
          k.TokenName[n.Keyword] = "Keyword";
          k.TokenName[n.NullLiteral] = "Null";
          k.TokenName[n.NumericLiteral] = "Numeric";
          k.TokenName[n.Punctuator] = "Punctuator";
          k.TokenName[n.StringLiteral] = "String";
          k.TokenName[n.RegularExpression] = "RegularExpression";
          k.TokenName[n.Template] = "Template"
        }, function(c, k, n) {
          var l = n(4),
            a = n(5),
            m = n(9),
            h = n(7);
          c = function() {
            function c(a, g) {
              this.source = a;
              this.errorHandler = g;
              this.trackComment = !1;
              this.length = a.length;
              this.index = 0;
              this.lineNumber = 0 < a.length ? 1 : 0;
              this.lineStart = 0;
              this.curlyStack = []
            }
            c.prototype.eof = function() {
              return this.index >= this.length
            };
            c.prototype.throwUnexpectedToken = function(e) {
              void 0 === e && (e = a.Messages.UnexpectedTokenIllegal);
              this.errorHandler.throwError(this.index, this.lineNumber, this.index - this.lineStart + 1, e)
            };
            c.prototype.tolerateUnexpectedToken = function() {
              this.errorHandler.tolerateError(this.index, this.lineNumber, this.index - this.lineStart + 1, a.Messages.UnexpectedTokenIllegal)
            };
            c.prototype.skipSingleLineComment = function(a) {
              if (this.trackComment) {
                var e = [];
                var f = this.index - a;
                var b = {
                  start: {
                    line: this.lineNumber,
                    column: this.index - this.lineStart - a
                  },
                  end: {}
                }
              }
              for (; !this.eof();) {
                var d = this.source.charCodeAt(this.index);
                ++this.index;
                if (m.Character.isLineTerminator(d)) return this.trackComment && (b.end = {
                  line: this.lineNumber,
                  column: this.index - this.lineStart - 1
                }, a = {
                  multiLine: !1,
                  slice: [f + a, this.index - 1],
                  range: [f, this.index - 1],
                  loc: b
                }, e.push(a)), 13 === d && 10 === this.source.charCodeAt(this.index) && ++this.index, ++this.lineNumber, this.lineStart = this.index, e
              }
              this.trackComment && (b.end = {
                line: this.lineNumber,
                column: this.index - this.lineStart
              }, a = {
                multiLine: !1,
                slice: [f + a, this.index],
                range: [f, this.index],
                loc: b
              }, e.push(a));
              return e
            };
            c.prototype.skipMultiLineComment =
              function() {
                if (this.trackComment) {
                  var a = [];
                  var g = this.index - 2;
                  var f = {
                    start: {
                      line: this.lineNumber,
                      column: this.index - this.lineStart - 2
                    },
                    end: {}
                  }
                }
                for (; !this.eof();) {
                  var b = this.source.charCodeAt(this.index);
                  if (m.Character.isLineTerminator(b)) 13 === b && 10 === this.source.charCodeAt(this.index + 1) && ++this.index, ++this.lineNumber, ++this.index, this.lineStart = this.index;
                  else {
                    if (42 === b && 47 === this.source.charCodeAt(this.index + 1)) return this.index += 2, this.trackComment && (f.end = {
                      line: this.lineNumber,
                      column: this.index -
                        this.lineStart
                    }, g = {
                      multiLine: !0,
                      slice: [g + 2, this.index - 2],
                      range: [g, this.index],
                      loc: f
                    }, a.push(g)), a;
                    ++this.index
                  }
                }
                this.trackComment && (f.end = {
                  line: this.lineNumber,
                  column: this.index - this.lineStart
                }, g = {
                  multiLine: !0,
                  slice: [g + 2, this.index],
                  range: [g, this.index],
                  loc: f
                }, a.push(g));
                this.tolerateUnexpectedToken();
                return a
              };
            c.prototype.scanComments = function() {
              var a;
              this.trackComment && (a = []);
              for (var g = 0 === this.index; !this.eof();) {
                var f = this.source.charCodeAt(this.index);
                if (m.Character.isWhiteSpace(f)) ++this.index;
                else if (m.Character.isLineTerminator(f)) ++this.index, 13 === f && 10 === this.source.charCodeAt(this.index) && ++this.index, ++this.lineNumber, this.lineStart = this.index, g = !0;
                else if (47 === f)
                  if (f = this.source.charCodeAt(this.index + 1), 47 === f) this.index += 2, f = this.skipSingleLineComment(2), this.trackComment && (a = a.concat(f)), g = !0;
                  else if (42 === f) this.index += 2, f = this.skipMultiLineComment(), this.trackComment && (a = a.concat(f));
                else break;
                else if (g && 45 === f)
                  if (45 === this.source.charCodeAt(this.index + 1) && 62 === this.source.charCodeAt(this.index +
                      2)) this.index += 3, f = this.skipSingleLineComment(3), this.trackComment && (a = a.concat(f));
                  else break;
                else if (60 === f)
                  if ("!--" === this.source.slice(this.index + 1, this.index + 4)) this.index += 4, f = this.skipSingleLineComment(4), this.trackComment && (a = a.concat(f));
                  else break;
                else break
              }
              return a
            };
            c.prototype.isFutureReservedWord = function(a) {
              switch (a) {
                case "enum":
                case "export":
                case "import":
                case "super":
                  return !0;
                default:
                  return !1
              }
            };
            c.prototype.isStrictModeReservedWord = function(a) {
              switch (a) {
                case "implements":
                case "interface":
                case "package":
                case "private":
                case "protected":
                case "public":
                case "static":
                case "yield":
                case "let":
                  return !0;
                default:
                  return !1
              }
            };
            c.prototype.isRestrictedWord = function(a) {
              return "eval" === a || "arguments" === a
            };
            c.prototype.isKeyword = function(a) {
              switch (a.length) {
                case 2:
                  return "if" === a || "in" === a || "do" === a;
                case 3:
                  return "var" === a || "for" === a || "new" === a || "try" === a || "let" === a;
                case 4:
                  return "this" === a || "else" === a || "case" === a || "void" === a || "with" === a || "enum" === a;
                case 5:
                  return "while" === a || "break" === a || "catch" === a || "throw" === a || "const" === a || "yield" === a || "class" === a || "super" === a;
                case 6:
                  return "return" === a || "typeof" === a || "delete" ===
                    a || "switch" === a || "export" === a || "import" === a;
                case 7:
                  return "default" === a || "finally" === a || "extends" === a;
                case 8:
                  return "function" === a || "continue" === a || "debugger" === a;
                case 10:
                  return "instanceof" === a;
                default:
                  return !1
              }
            };
            c.prototype.codePointAt = function(a) {
              var e = this.source.charCodeAt(a);
              55296 <= e && 56319 >= e && (a = this.source.charCodeAt(a + 1), 56320 <= a && 57343 >= a && (e = 1024 * (e - 55296) + a - 56320 + 65536));
              return e
            };
            c.prototype.scanHexEscape = function(a) {
              a = "u" === a ? 4 : 2;
              for (var e = 0, f = 0; f < a; ++f)
                if (!this.eof() && m.Character.isHexDigit(this.source.charCodeAt(this.index))) e =
                  16 * e + "0123456789abcdef".indexOf(this.source[this.index++].toLowerCase());
                else return "";
              return String.fromCharCode(e)
            };
            c.prototype.scanUnicodeCodePointEscape = function() {
              var a = this.source[this.index],
                g = 0;
              for ("}" === a && this.throwUnexpectedToken(); !this.eof();) {
                a = this.source[this.index++];
                if (!m.Character.isHexDigit(a.charCodeAt(0))) break;
                g = 16 * g + "0123456789abcdef".indexOf(a.toLowerCase())
              }(1114111 < g || "}" !== a) && this.throwUnexpectedToken();
              return m.Character.fromCodePoint(g)
            };
            c.prototype.getIdentifier = function() {
              for (var a =
                  this.index++; !this.eof();) {
                var g = this.source.charCodeAt(this.index);
                if (92 === g || 55296 <= g && 57343 > g) return this.index = a, this.getComplexIdentifier();
                if (m.Character.isIdentifierPart(g)) ++this.index;
                else break
              }
              return this.source.slice(a, this.index)
            };
            c.prototype.getComplexIdentifier = function() {
              var a = this.codePointAt(this.index),
                g = m.Character.fromCodePoint(a);
              this.index += g.length;
              if (92 === a) {
                117 !== this.source.charCodeAt(this.index) && this.throwUnexpectedToken();
                ++this.index;
                if ("{" === this.source[this.index]) {
                  ++this.index;
                  var f = this.scanUnicodeCodePointEscape()
                } else f = this.scanHexEscape("u"), a = f.charCodeAt(0), f && "\\" !== f && m.Character.isIdentifierStart(a) || this.throwUnexpectedToken();
                g = f
              }
              for (; !this.eof();) {
                a = this.codePointAt(this.index);
                if (!m.Character.isIdentifierPart(a)) break;
                f = m.Character.fromCodePoint(a);
                g += f;
                this.index += f.length;
                92 === a && (g = g.substr(0, g.length - 1), 117 !== this.source.charCodeAt(this.index) && this.throwUnexpectedToken(), ++this.index, "{" === this.source[this.index] ? (++this.index, f = this.scanUnicodeCodePointEscape()) :
                  (f = this.scanHexEscape("u"), a = f.charCodeAt(0), f && "\\" !== f && m.Character.isIdentifierPart(a) || this.throwUnexpectedToken()), g += f)
              }
              return g
            };
            c.prototype.octalToDecimal = function(a) {
              var e = "0" !== a,
                f = "01234567".indexOf(a);
              !this.eof() && m.Character.isOctalDigit(this.source.charCodeAt(this.index)) && (e = !0, f = 8 * f + "01234567".indexOf(this.source[this.index++]), 0 <= "0123".indexOf(a) && !this.eof() && m.Character.isOctalDigit(this.source.charCodeAt(this.index)) && (f = 8 * f + "01234567".indexOf(this.source[this.index++])));
              return {
                code: f,
                octal: e
              }
            };
            c.prototype.scanIdentifier = function() {
              var a = this.index,
                g = 92 === this.source.charCodeAt(a) ? this.getComplexIdentifier() : this.getIdentifier();
              return {
                type: 1 === g.length ? h.Token.Identifier : this.isKeyword(g) ? h.Token.Keyword : "null" === g ? h.Token.NullLiteral : "true" === g || "false" === g ? h.Token.BooleanLiteral : h.Token.Identifier,
                value: g,
                lineNumber: this.lineNumber,
                lineStart: this.lineStart,
                start: a,
                end: this.index
              }
            };
            c.prototype.scanPunctuator = function() {
              var a = {
                  type: h.Token.Punctuator,
                  value: "",
                  lineNumber: this.lineNumber,
                  lineStart: this.lineStart,
                  start: this.index,
                  end: this.index
                },
                g = this.source[this.index];
              switch (g) {
                case "(":
                case "{":
                  "{" === g && this.curlyStack.push("{");
                  ++this.index;
                  break;
                case ".":
                  ++this.index;
                  "." === this.source[this.index] && "." === this.source[this.index + 1] && (this.index += 2, g = "...");
                  break;
                case "}":
                  ++this.index;
                  this.curlyStack.pop();
                  break;
                case ")":
                case ";":
                case ",":
                case "[":
                case "]":
                case ":":
                case "?":
                case "~":
                  ++this.index;
                  break;
                default:
                  g = this.source.substr(this.index, 4), ">>>=" === g ? this.index += 4 : (g = g.substr(0,
                    3), "===" === g || "!==" === g || ">>>" === g || "<<=" === g || ">>=" === g || "**=" === g ? this.index += 3 : (g = g.substr(0, 2), "&&" === g || "||" === g || "==" === g || "!=" === g || "+=" === g || "-=" === g || "*=" === g || "/=" === g || "++" === g || "--" === g || "<<" === g || ">>" === g || "&=" === g || "|=" === g || "^=" === g || "%=" === g || "<=" === g || ">=" === g || "=>" === g || "**" === g ? this.index += 2 : (g = this.source[this.index], 0 <= "<>=!+-*%&|^/".indexOf(g) && ++this.index)))
              }
              this.index === a.start && this.throwUnexpectedToken();
              a.end = this.index;
              a.value = g;
              return a
            };
            c.prototype.scanHexLiteral = function(a) {
              for (var e =
                  ""; !this.eof() && m.Character.isHexDigit(this.source.charCodeAt(this.index));) e += this.source[this.index++];
              0 === e.length && this.throwUnexpectedToken();
              m.Character.isIdentifierStart(this.source.charCodeAt(this.index)) && this.throwUnexpectedToken();
              return {
                type: h.Token.NumericLiteral,
                value: parseInt("0x" + e, 16),
                lineNumber: this.lineNumber,
                lineStart: this.lineStart,
                start: a,
                end: this.index
              }
            };
            c.prototype.scanBinaryLiteral = function(a) {
              for (var e = "", f; !this.eof();) {
                f = this.source[this.index];
                if ("0" !== f && "1" !== f) break;
                e += this.source[this.index++]
              }
              0 === e.length && this.throwUnexpectedToken();
              this.eof() || (f = this.source.charCodeAt(this.index), (m.Character.isIdentifierStart(f) || m.Character.isDecimalDigit(f)) && this.throwUnexpectedToken());
              return {
                type: h.Token.NumericLiteral,
                value: parseInt(e, 2),
                lineNumber: this.lineNumber,
                lineStart: this.lineStart,
                start: a,
                end: this.index
              }
            };
            c.prototype.scanOctalLiteral = function(a, g) {
              var e = "",
                b = !1;
              m.Character.isOctalDigit(a.charCodeAt(0)) ? (b = !0, e = "0" + this.source[this.index++]) : ++this.index;
              for (; !this.eof() &&
                m.Character.isOctalDigit(this.source.charCodeAt(this.index));) e += this.source[this.index++];
              b || 0 !== e.length || this.throwUnexpectedToken();
              (m.Character.isIdentifierStart(this.source.charCodeAt(this.index)) || m.Character.isDecimalDigit(this.source.charCodeAt(this.index))) && this.throwUnexpectedToken();
              return {
                type: h.Token.NumericLiteral,
                value: parseInt(e, 8),
                octal: b,
                lineNumber: this.lineNumber,
                lineStart: this.lineStart,
                start: g,
                end: this.index
              }
            };
            c.prototype.isImplicitOctalLiteral = function() {
              for (var a = this.index +
                  1; a < this.length; ++a) {
                var g = this.source[a];
                if ("8" === g || "9" === g) return !1;
                if (!m.Character.isOctalDigit(g.charCodeAt(0))) break
              }
              return !0
            };
            c.prototype.scanNumericLiteral = function() {
              var a = this.index,
                g = this.source[a];
              l.assert(m.Character.isDecimalDigit(g.charCodeAt(0)) || "." === g, "Numeric literal must start with a decimal digit or a decimal point");
              var f = "";
              if ("." !== g) {
                f = this.source[this.index++];
                g = this.source[this.index];
                if ("0" === f) {
                  if ("x" === g || "X" === g) return ++this.index, this.scanHexLiteral(a);
                  if ("b" === g ||
                    "B" === g) return ++this.index, this.scanBinaryLiteral(a);
                  if ("o" === g || "O" === g || g && m.Character.isOctalDigit(g.charCodeAt(0)) && this.isImplicitOctalLiteral()) return this.scanOctalLiteral(g, a)
                }
                for (; m.Character.isDecimalDigit(this.source.charCodeAt(this.index));) f += this.source[this.index++];
                g = this.source[this.index]
              }
              if ("." === g) {
                for (f += this.source[this.index++]; m.Character.isDecimalDigit(this.source.charCodeAt(this.index));) f += this.source[this.index++];
                g = this.source[this.index]
              }
              if ("e" === g || "E" === g) {
                f += this.source[this.index++];
                g = this.source[this.index];
                if ("+" === g || "-" === g) f += this.source[this.index++];
                if (m.Character.isDecimalDigit(this.source.charCodeAt(this.index)))
                  for (; m.Character.isDecimalDigit(this.source.charCodeAt(this.index));) f += this.source[this.index++];
                else this.throwUnexpectedToken()
              }
              m.Character.isIdentifierStart(this.source.charCodeAt(this.index)) && this.throwUnexpectedToken();
              return {
                type: h.Token.NumericLiteral,
                value: parseFloat(f),
                lineNumber: this.lineNumber,
                lineStart: this.lineStart,
                start: a,
                end: this.index
              }
            };
            c.prototype.scanStringLiteral =
              function() {
                var a = this.index,
                  g = this.source[a];
                l.assert("'" === g || '"' === g, "String literal must starts with a quote");
                ++this.index;
                for (var f = !1, b = ""; !this.eof();) {
                  var d = this.source[this.index++];
                  if (d === g) {
                    g = "";
                    break
                  } else if ("\\" === d)
                    if ((d = this.source[this.index++]) && m.Character.isLineTerminator(d.charCodeAt(0))) ++this.lineNumber, "\r" === d && "\n" === this.source[this.index] && ++this.index, this.lineStart = this.index;
                    else switch (d) {
                        case "u":
                        case "x":
                          "{" === this.source[this.index] ? (++this.index, b += this.scanUnicodeCodePointEscape()) :
                            ((d = this.scanHexEscape(d)) || this.throwUnexpectedToken(), b += d);
                          break;
                        case "n":
                          b += "\n";
                          break;
                        case "r":
                          b += "\r";
                          break;
                        case "t":
                          b += "\t";
                          break;
                        case "b":
                          b += "\b";
                          break;
                        case "f":
                          b += "\f";
                          break;
                        case "v":
                          b += "\x0B";
                          break;
                        case "8":
                        case "9":
                          b += d;
                          this.tolerateUnexpectedToken();
                          break;
                        default:
                          d && m.Character.isOctalDigit(d.charCodeAt(0)) ? (d = this.octalToDecimal(d), f = d.octal || f, b += String.fromCharCode(d.code)) : b += d
                      } else if (m.Character.isLineTerminator(d.charCodeAt(0))) break;
                      else b += d
                }
                "" !== g && (this.index = a, this.throwUnexpectedToken());
                return {
                  type: h.Token.StringLiteral,
                  value: b,
                  octal: f,
                  lineNumber: this.lineNumber,
                  lineStart: this.lineStart,
                  start: a,
                  end: this.index
                }
              };
            c.prototype.scanTemplate = function() {
              var e = "",
                g = !1,
                f = this.index,
                b = "`" === this.source[f],
                d = !1,
                c = 2;
              for (++this.index; !this.eof();) {
                var k = this.source[this.index++];
                if ("`" === k) {
                  c = 1;
                  g = d = !0;
                  break
                } else if ("$" === k) {
                  if ("{" === this.source[this.index]) {
                    this.curlyStack.push("${");
                    ++this.index;
                    g = !0;
                    break
                  }
                  e += k
                } else if ("\\" === k)
                  if (k = this.source[this.index++], m.Character.isLineTerminator(k.charCodeAt(0))) ++this.lineNumber,
                    "\r" === k && "\n" === this.source[this.index] && ++this.index, this.lineStart = this.index;
                  else switch (k) {
                    case "n":
                      e += "\n";
                      break;
                    case "r":
                      e += "\r";
                      break;
                    case "t":
                      e += "\t";
                      break;
                    case "u":
                    case "x":
                      if ("{" === this.source[this.index]) ++this.index, e += this.scanUnicodeCodePointEscape();
                      else {
                        var l = this.index,
                          n = this.scanHexEscape(k);
                        n ? e += n : (this.index = l, e += k)
                      }
                      break;
                    case "b":
                      e += "\b";
                      break;
                    case "f":
                      e += "\f";
                      break;
                    case "v":
                      e += "\v";
                      break;
                    default:
                      "0" === k ? (m.Character.isDecimalDigit(this.source.charCodeAt(this.index)) && this.throwUnexpectedToken(a.Messages.TemplateOctalLiteral),
                        e += "\x00") : m.Character.isOctalDigit(k.charCodeAt(0)) ? this.throwUnexpectedToken(a.Messages.TemplateOctalLiteral) : e += k
                  } else m.Character.isLineTerminator(k.charCodeAt(0)) ? (++this.lineNumber, "\r" === k && "\n" === this.source[this.index] && ++this.index, this.lineStart = this.index, e += "\n") : e += k
              }
              g || this.throwUnexpectedToken();
              b || this.curlyStack.pop();
              return {
                type: h.Token.Template,
                value: {
                  cooked: e,
                  raw: this.source.slice(f + 1, this.index - c)
                },
                head: b,
                tail: d,
                lineNumber: this.lineNumber,
                lineStart: this.lineStart,
                start: f,
                end: this.index
              }
            };
            c.prototype.testRegExp = function(e, g) {
              var f = e,
                b = this;
              0 <= g.indexOf("u") && (f = f.replace(/\\u\{([0-9a-fA-F]+)\}|\\u([a-fA-F0-9]{4})/g, function(e, f, g) {
                e = parseInt(f || g, 16);
                1114111 < e && b.throwUnexpectedToken(a.Messages.InvalidRegExp);
                return 65535 >= e ? String.fromCharCode(e) : "\uffff"
              }).replace(/[\uD800-\uDBFF][\uDC00-\uDFFF]/g, "\uffff"));
              try {
                RegExp(f)
              } catch (d) {
                this.throwUnexpectedToken(a.Messages.InvalidRegExp)
              }
              try {
                return new RegExp(e, g)
              } catch (d) {
                return null
              }
            };
            c.prototype.scanRegExpBody = function() {
              var e = this.source[this.index];
              l.assert("/" === e, "Regular expression literal must start with a slash");
              for (var g = this.source[this.index++], f = !1, b = !1; !this.eof();)
                if (e = this.source[this.index++], g += e, "\\" === e) e = this.source[this.index++], m.Character.isLineTerminator(e.charCodeAt(0)) && this.throwUnexpectedToken(a.Messages.UnterminatedRegExp), g += e;
                else if (m.Character.isLineTerminator(e.charCodeAt(0))) this.throwUnexpectedToken(a.Messages.UnterminatedRegExp);
              else if (f) "]" === e && (f = !1);
              else if ("/" === e) {
                b = !0;
                break
              } else "[" === e && (f = !0);
              b || this.throwUnexpectedToken(a.Messages.UnterminatedRegExp);
              return {
                value: g.substr(1, g.length - 2),
                literal: g
              }
            };
            c.prototype.scanRegExpFlags = function() {
              for (var a = "", g = ""; !this.eof();) {
                var f = this.source[this.index];
                if (!m.Character.isIdentifierPart(f.charCodeAt(0))) break;
                ++this.index;
                if ("\\" !== f || this.eof()) g += f, a += f;
                else {
                  f = this.source[this.index];
                  if ("u" === f) {
                    ++this.index;
                    var b = this.index;
                    if (f = this.scanHexEscape("u"))
                      for (g += f, a += "\\u"; b < this.index; ++b) a += this.source[b];
                    else this.index = b, g += "u", a += "\\u"
                  } else a += "\\";
                  this.tolerateUnexpectedToken()
                }
              }
              return {
                value: g,
                literal: a
              }
            };
            c.prototype.scanRegExp = function() {
              var a = this.index,
                g = this.scanRegExpBody(),
                f = this.scanRegExpFlags(),
                b = this.testRegExp(g.value, f.value);
              return {
                type: h.Token.RegularExpression,
                value: b,
                literal: g.literal + f.literal,
                regex: {
                  pattern: g.value,
                  flags: f.value
                },
                lineNumber: this.lineNumber,
                lineStart: this.lineStart,
                start: a,
                end: this.index
              }
            };
            c.prototype.lex = function() {
              if (this.eof()) return {
                type: h.Token.EOF,
                lineNumber: this.lineNumber,
                lineStart: this.lineStart,
                start: this.index,
                end: this.index
              };
              var a = this.source.charCodeAt(this.index);
              return m.Character.isIdentifierStart(a) ? this.scanIdentifier() : 40 === a || 41 === a || 59 === a ? this.scanPunctuator() : 39 === a || 34 === a ? this.scanStringLiteral() : 46 === a ? m.Character.isDecimalDigit(this.source.charCodeAt(this.index + 1)) ? this.scanNumericLiteral() : this.scanPunctuator() : m.Character.isDecimalDigit(a) ? this.scanNumericLiteral() : 96 === a || 125 === a && "${" === this.curlyStack[this.curlyStack.length - 1] ? this.scanTemplate() : 55296 <= a && 57343 > a && m.Character.isIdentifierStart(this.codePointAt(this.index)) ? this.scanIdentifier() :
                this.scanPunctuator()
            };
            return c
          }();
          k.Scanner = c
        }, function(c, k) {
          var n = /[\xAA\xB5\xBA\xC0-\xD6\xD8-\xF6\xF8-\u02C1\u02C6-\u02D1\u02E0-\u02E4\u02EC\u02EE\u0370-\u0374\u0376\u0377\u037A-\u037D\u037F\u0386\u0388-\u038A\u038C\u038E-\u03A1\u03A3-\u03F5\u03F7-\u0481\u048A-\u052F\u0531-\u0556\u0559\u0561-\u0587\u05D0-\u05EA\u05F0-\u05F2\u0620-\u064A\u066E\u066F\u0671-\u06D3\u06D5\u06E5\u06E6\u06EE\u06EF\u06FA-\u06FC\u06FF\u0710\u0712-\u072F\u074D-\u07A5\u07B1\u07CA-\u07EA\u07F4\u07F5\u07FA\u0800-\u0815\u081A\u0824\u0828\u0840-\u0858\u08A0-\u08B4\u0904-\u0939\u093D\u0950\u0958-\u0961\u0971-\u0980\u0985-\u098C\u098F\u0990\u0993-\u09A8\u09AA-\u09B0\u09B2\u09B6-\u09B9\u09BD\u09CE\u09DC\u09DD\u09DF-\u09E1\u09F0\u09F1\u0A05-\u0A0A\u0A0F\u0A10\u0A13-\u0A28\u0A2A-\u0A30\u0A32\u0A33\u0A35\u0A36\u0A38\u0A39\u0A59-\u0A5C\u0A5E\u0A72-\u0A74\u0A85-\u0A8D\u0A8F-\u0A91\u0A93-\u0AA8\u0AAA-\u0AB0\u0AB2\u0AB3\u0AB5-\u0AB9\u0ABD\u0AD0\u0AE0\u0AE1\u0AF9\u0B05-\u0B0C\u0B0F\u0B10\u0B13-\u0B28\u0B2A-\u0B30\u0B32\u0B33\u0B35-\u0B39\u0B3D\u0B5C\u0B5D\u0B5F-\u0B61\u0B71\u0B83\u0B85-\u0B8A\u0B8E-\u0B90\u0B92-\u0B95\u0B99\u0B9A\u0B9C\u0B9E\u0B9F\u0BA3\u0BA4\u0BA8-\u0BAA\u0BAE-\u0BB9\u0BD0\u0C05-\u0C0C\u0C0E-\u0C10\u0C12-\u0C28\u0C2A-\u0C39\u0C3D\u0C58-\u0C5A\u0C60\u0C61\u0C85-\u0C8C\u0C8E-\u0C90\u0C92-\u0CA8\u0CAA-\u0CB3\u0CB5-\u0CB9\u0CBD\u0CDE\u0CE0\u0CE1\u0CF1\u0CF2\u0D05-\u0D0C\u0D0E-\u0D10\u0D12-\u0D3A\u0D3D\u0D4E\u0D5F-\u0D61\u0D7A-\u0D7F\u0D85-\u0D96\u0D9A-\u0DB1\u0DB3-\u0DBB\u0DBD\u0DC0-\u0DC6\u0E01-\u0E30\u0E32\u0E33\u0E40-\u0E46\u0E81\u0E82\u0E84\u0E87\u0E88\u0E8A\u0E8D\u0E94-\u0E97\u0E99-\u0E9F\u0EA1-\u0EA3\u0EA5\u0EA7\u0EAA\u0EAB\u0EAD-\u0EB0\u0EB2\u0EB3\u0EBD\u0EC0-\u0EC4\u0EC6\u0EDC-\u0EDF\u0F00\u0F40-\u0F47\u0F49-\u0F6C\u0F88-\u0F8C\u1000-\u102A\u103F\u1050-\u1055\u105A-\u105D\u1061\u1065\u1066\u106E-\u1070\u1075-\u1081\u108E\u10A0-\u10C5\u10C7\u10CD\u10D0-\u10FA\u10FC-\u1248\u124A-\u124D\u1250-\u1256\u1258\u125A-\u125D\u1260-\u1288\u128A-\u128D\u1290-\u12B0\u12B2-\u12B5\u12B8-\u12BE\u12C0\u12C2-\u12C5\u12C8-\u12D6\u12D8-\u1310\u1312-\u1315\u1318-\u135A\u1380-\u138F\u13A0-\u13F5\u13F8-\u13FD\u1401-\u166C\u166F-\u167F\u1681-\u169A\u16A0-\u16EA\u16EE-\u16F8\u1700-\u170C\u170E-\u1711\u1720-\u1731\u1740-\u1751\u1760-\u176C\u176E-\u1770\u1780-\u17B3\u17D7\u17DC\u1820-\u1877\u1880-\u18A8\u18AA\u18B0-\u18F5\u1900-\u191E\u1950-\u196D\u1970-\u1974\u1980-\u19AB\u19B0-\u19C9\u1A00-\u1A16\u1A20-\u1A54\u1AA7\u1B05-\u1B33\u1B45-\u1B4B\u1B83-\u1BA0\u1BAE\u1BAF\u1BBA-\u1BE5\u1C00-\u1C23\u1C4D-\u1C4F\u1C5A-\u1C7D\u1CE9-\u1CEC\u1CEE-\u1CF1\u1CF5\u1CF6\u1D00-\u1DBF\u1E00-\u1F15\u1F18-\u1F1D\u1F20-\u1F45\u1F48-\u1F4D\u1F50-\u1F57\u1F59\u1F5B\u1F5D\u1F5F-\u1F7D\u1F80-\u1FB4\u1FB6-\u1FBC\u1FBE\u1FC2-\u1FC4\u1FC6-\u1FCC\u1FD0-\u1FD3\u1FD6-\u1FDB\u1FE0-\u1FEC\u1FF2-\u1FF4\u1FF6-\u1FFC\u2071\u207F\u2090-\u209C\u2102\u2107\u210A-\u2113\u2115\u2118-\u211D\u2124\u2126\u2128\u212A-\u2139\u213C-\u213F\u2145-\u2149\u214E\u2160-\u2188\u2C00-\u2C2E\u2C30-\u2C5E\u2C60-\u2CE4\u2CEB-\u2CEE\u2CF2\u2CF3\u2D00-\u2D25\u2D27\u2D2D\u2D30-\u2D67\u2D6F\u2D80-\u2D96\u2DA0-\u2DA6\u2DA8-\u2DAE\u2DB0-\u2DB6\u2DB8-\u2DBE\u2DC0-\u2DC6\u2DC8-\u2DCE\u2DD0-\u2DD6\u2DD8-\u2DDE\u3005-\u3007\u3021-\u3029\u3031-\u3035\u3038-\u303C\u3041-\u3096\u309B-\u309F\u30A1-\u30FA\u30FC-\u30FF\u3105-\u312D\u3131-\u318E\u31A0-\u31BA\u31F0-\u31FF\u3400-\u4DB5\u4E00-\u9FD5\uA000-\uA48C\uA4D0-\uA4FD\uA500-\uA60C\uA610-\uA61F\uA62A\uA62B\uA640-\uA66E\uA67F-\uA69D\uA6A0-\uA6EF\uA717-\uA71F\uA722-\uA788\uA78B-\uA7AD\uA7B0-\uA7B7\uA7F7-\uA801\uA803-\uA805\uA807-\uA80A\uA80C-\uA822\uA840-\uA873\uA882-\uA8B3\uA8F2-\uA8F7\uA8FB\uA8FD\uA90A-\uA925\uA930-\uA946\uA960-\uA97C\uA984-\uA9B2\uA9CF\uA9E0-\uA9E4\uA9E6-\uA9EF\uA9FA-\uA9FE\uAA00-\uAA28\uAA40-\uAA42\uAA44-\uAA4B\uAA60-\uAA76\uAA7A\uAA7E-\uAAAF\uAAB1\uAAB5\uAAB6\uAAB9-\uAABD\uAAC0\uAAC2\uAADB-\uAADD\uAAE0-\uAAEA\uAAF2-\uAAF4\uAB01-\uAB06\uAB09-\uAB0E\uAB11-\uAB16\uAB20-\uAB26\uAB28-\uAB2E\uAB30-\uAB5A\uAB5C-\uAB65\uAB70-\uABE2\uAC00-\uD7A3\uD7B0-\uD7C6\uD7CB-\uD7FB\uF900-\uFA6D\uFA70-\uFAD9\uFB00-\uFB06\uFB13-\uFB17\uFB1D\uFB1F-\uFB28\uFB2A-\uFB36\uFB38-\uFB3C\uFB3E\uFB40\uFB41\uFB43\uFB44\uFB46-\uFBB1\uFBD3-\uFD3D\uFD50-\uFD8F\uFD92-\uFDC7\uFDF0-\uFDFB\uFE70-\uFE74\uFE76-\uFEFC\uFF21-\uFF3A\uFF41-\uFF5A\uFF66-\uFFBE\uFFC2-\uFFC7\uFFCA-\uFFCF\uFFD2-\uFFD7\uFFDA-\uFFDC]|\uD800[\uDC00-\uDC0B\uDC0D-\uDC26\uDC28-\uDC3A\uDC3C\uDC3D\uDC3F-\uDC4D\uDC50-\uDC5D\uDC80-\uDCFA\uDD40-\uDD74\uDE80-\uDE9C\uDEA0-\uDED0\uDF00-\uDF1F\uDF30-\uDF4A\uDF50-\uDF75\uDF80-\uDF9D\uDFA0-\uDFC3\uDFC8-\uDFCF\uDFD1-\uDFD5]|\uD801[\uDC00-\uDC9D\uDD00-\uDD27\uDD30-\uDD63\uDE00-\uDF36\uDF40-\uDF55\uDF60-\uDF67]|\uD802[\uDC00-\uDC05\uDC08\uDC0A-\uDC35\uDC37\uDC38\uDC3C\uDC3F-\uDC55\uDC60-\uDC76\uDC80-\uDC9E\uDCE0-\uDCF2\uDCF4\uDCF5\uDD00-\uDD15\uDD20-\uDD39\uDD80-\uDDB7\uDDBE\uDDBF\uDE00\uDE10-\uDE13\uDE15-\uDE17\uDE19-\uDE33\uDE60-\uDE7C\uDE80-\uDE9C\uDEC0-\uDEC7\uDEC9-\uDEE4\uDF00-\uDF35\uDF40-\uDF55\uDF60-\uDF72\uDF80-\uDF91]|\uD803[\uDC00-\uDC48\uDC80-\uDCB2\uDCC0-\uDCF2]|\uD804[\uDC03-\uDC37\uDC83-\uDCAF\uDCD0-\uDCE8\uDD03-\uDD26\uDD50-\uDD72\uDD76\uDD83-\uDDB2\uDDC1-\uDDC4\uDDDA\uDDDC\uDE00-\uDE11\uDE13-\uDE2B\uDE80-\uDE86\uDE88\uDE8A-\uDE8D\uDE8F-\uDE9D\uDE9F-\uDEA8\uDEB0-\uDEDE\uDF05-\uDF0C\uDF0F\uDF10\uDF13-\uDF28\uDF2A-\uDF30\uDF32\uDF33\uDF35-\uDF39\uDF3D\uDF50\uDF5D-\uDF61]|\uD805[\uDC80-\uDCAF\uDCC4\uDCC5\uDCC7\uDD80-\uDDAE\uDDD8-\uDDDB\uDE00-\uDE2F\uDE44\uDE80-\uDEAA\uDF00-\uDF19]|\uD806[\uDCA0-\uDCDF\uDCFF\uDEC0-\uDEF8]|\uD808[\uDC00-\uDF99]|\uD809[\uDC00-\uDC6E\uDC80-\uDD43]|[\uD80C\uD840-\uD868\uD86A-\uD86C\uD86F-\uD872][\uDC00-\uDFFF]|\uD80D[\uDC00-\uDC2E]|\uD811[\uDC00-\uDE46]|\uD81A[\uDC00-\uDE38\uDE40-\uDE5E\uDED0-\uDEED\uDF00-\uDF2F\uDF40-\uDF43\uDF63-\uDF77\uDF7D-\uDF8F]|\uD81B[\uDF00-\uDF44\uDF50\uDF93-\uDF9F]|\uD82C[\uDC00\uDC01]|\uD82F[\uDC00-\uDC6A\uDC70-\uDC7C\uDC80-\uDC88\uDC90-\uDC99]|\uD835[\uDC00-\uDC54\uDC56-\uDC9C\uDC9E\uDC9F\uDCA2\uDCA5\uDCA6\uDCA9-\uDCAC\uDCAE-\uDCB9\uDCBB\uDCBD-\uDCC3\uDCC5-\uDD05\uDD07-\uDD0A\uDD0D-\uDD14\uDD16-\uDD1C\uDD1E-\uDD39\uDD3B-\uDD3E\uDD40-\uDD44\uDD46\uDD4A-\uDD50\uDD52-\uDEA5\uDEA8-\uDEC0\uDEC2-\uDEDA\uDEDC-\uDEFA\uDEFC-\uDF14\uDF16-\uDF34\uDF36-\uDF4E\uDF50-\uDF6E\uDF70-\uDF88\uDF8A-\uDFA8\uDFAA-\uDFC2\uDFC4-\uDFCB]|\uD83A[\uDC00-\uDCC4]|\uD83B[\uDE00-\uDE03\uDE05-\uDE1F\uDE21\uDE22\uDE24\uDE27\uDE29-\uDE32\uDE34-\uDE37\uDE39\uDE3B\uDE42\uDE47\uDE49\uDE4B\uDE4D-\uDE4F\uDE51\uDE52\uDE54\uDE57\uDE59\uDE5B\uDE5D\uDE5F\uDE61\uDE62\uDE64\uDE67-\uDE6A\uDE6C-\uDE72\uDE74-\uDE77\uDE79-\uDE7C\uDE7E\uDE80-\uDE89\uDE8B-\uDE9B\uDEA1-\uDEA3\uDEA5-\uDEA9\uDEAB-\uDEBB]|\uD869[\uDC00-\uDED6\uDF00-\uDFFF]|\uD86D[\uDC00-\uDF34\uDF40-\uDFFF]|\uD86E[\uDC00-\uDC1D\uDC20-\uDFFF]|\uD873[\uDC00-\uDEA1]|\uD87E[\uDC00-\uDE1D]/,
            l = /[\xAA\xB5\xB7\xBA\xC0-\xD6\xD8-\xF6\xF8-\u02C1\u02C6-\u02D1\u02E0-\u02E4\u02EC\u02EE\u0300-\u0374\u0376\u0377\u037A-\u037D\u037F\u0386-\u038A\u038C\u038E-\u03A1\u03A3-\u03F5\u03F7-\u0481\u0483-\u0487\u048A-\u052F\u0531-\u0556\u0559\u0561-\u0587\u0591-\u05BD\u05BF\u05C1\u05C2\u05C4\u05C5\u05C7\u05D0-\u05EA\u05F0-\u05F2\u0610-\u061A\u0620-\u0669\u066E-\u06D3\u06D5-\u06DC\u06DF-\u06E8\u06EA-\u06FC\u06FF\u0710-\u074A\u074D-\u07B1\u07C0-\u07F5\u07FA\u0800-\u082D\u0840-\u085B\u08A0-\u08B4\u08E3-\u0963\u0966-\u096F\u0971-\u0983\u0985-\u098C\u098F\u0990\u0993-\u09A8\u09AA-\u09B0\u09B2\u09B6-\u09B9\u09BC-\u09C4\u09C7\u09C8\u09CB-\u09CE\u09D7\u09DC\u09DD\u09DF-\u09E3\u09E6-\u09F1\u0A01-\u0A03\u0A05-\u0A0A\u0A0F\u0A10\u0A13-\u0A28\u0A2A-\u0A30\u0A32\u0A33\u0A35\u0A36\u0A38\u0A39\u0A3C\u0A3E-\u0A42\u0A47\u0A48\u0A4B-\u0A4D\u0A51\u0A59-\u0A5C\u0A5E\u0A66-\u0A75\u0A81-\u0A83\u0A85-\u0A8D\u0A8F-\u0A91\u0A93-\u0AA8\u0AAA-\u0AB0\u0AB2\u0AB3\u0AB5-\u0AB9\u0ABC-\u0AC5\u0AC7-\u0AC9\u0ACB-\u0ACD\u0AD0\u0AE0-\u0AE3\u0AE6-\u0AEF\u0AF9\u0B01-\u0B03\u0B05-\u0B0C\u0B0F\u0B10\u0B13-\u0B28\u0B2A-\u0B30\u0B32\u0B33\u0B35-\u0B39\u0B3C-\u0B44\u0B47\u0B48\u0B4B-\u0B4D\u0B56\u0B57\u0B5C\u0B5D\u0B5F-\u0B63\u0B66-\u0B6F\u0B71\u0B82\u0B83\u0B85-\u0B8A\u0B8E-\u0B90\u0B92-\u0B95\u0B99\u0B9A\u0B9C\u0B9E\u0B9F\u0BA3\u0BA4\u0BA8-\u0BAA\u0BAE-\u0BB9\u0BBE-\u0BC2\u0BC6-\u0BC8\u0BCA-\u0BCD\u0BD0\u0BD7\u0BE6-\u0BEF\u0C00-\u0C03\u0C05-\u0C0C\u0C0E-\u0C10\u0C12-\u0C28\u0C2A-\u0C39\u0C3D-\u0C44\u0C46-\u0C48\u0C4A-\u0C4D\u0C55\u0C56\u0C58-\u0C5A\u0C60-\u0C63\u0C66-\u0C6F\u0C81-\u0C83\u0C85-\u0C8C\u0C8E-\u0C90\u0C92-\u0CA8\u0CAA-\u0CB3\u0CB5-\u0CB9\u0CBC-\u0CC4\u0CC6-\u0CC8\u0CCA-\u0CCD\u0CD5\u0CD6\u0CDE\u0CE0-\u0CE3\u0CE6-\u0CEF\u0CF1\u0CF2\u0D01-\u0D03\u0D05-\u0D0C\u0D0E-\u0D10\u0D12-\u0D3A\u0D3D-\u0D44\u0D46-\u0D48\u0D4A-\u0D4E\u0D57\u0D5F-\u0D63\u0D66-\u0D6F\u0D7A-\u0D7F\u0D82\u0D83\u0D85-\u0D96\u0D9A-\u0DB1\u0DB3-\u0DBB\u0DBD\u0DC0-\u0DC6\u0DCA\u0DCF-\u0DD4\u0DD6\u0DD8-\u0DDF\u0DE6-\u0DEF\u0DF2\u0DF3\u0E01-\u0E3A\u0E40-\u0E4E\u0E50-\u0E59\u0E81\u0E82\u0E84\u0E87\u0E88\u0E8A\u0E8D\u0E94-\u0E97\u0E99-\u0E9F\u0EA1-\u0EA3\u0EA5\u0EA7\u0EAA\u0EAB\u0EAD-\u0EB9\u0EBB-\u0EBD\u0EC0-\u0EC4\u0EC6\u0EC8-\u0ECD\u0ED0-\u0ED9\u0EDC-\u0EDF\u0F00\u0F18\u0F19\u0F20-\u0F29\u0F35\u0F37\u0F39\u0F3E-\u0F47\u0F49-\u0F6C\u0F71-\u0F84\u0F86-\u0F97\u0F99-\u0FBC\u0FC6\u1000-\u1049\u1050-\u109D\u10A0-\u10C5\u10C7\u10CD\u10D0-\u10FA\u10FC-\u1248\u124A-\u124D\u1250-\u1256\u1258\u125A-\u125D\u1260-\u1288\u128A-\u128D\u1290-\u12B0\u12B2-\u12B5\u12B8-\u12BE\u12C0\u12C2-\u12C5\u12C8-\u12D6\u12D8-\u1310\u1312-\u1315\u1318-\u135A\u135D-\u135F\u1369-\u1371\u1380-\u138F\u13A0-\u13F5\u13F8-\u13FD\u1401-\u166C\u166F-\u167F\u1681-\u169A\u16A0-\u16EA\u16EE-\u16F8\u1700-\u170C\u170E-\u1714\u1720-\u1734\u1740-\u1753\u1760-\u176C\u176E-\u1770\u1772\u1773\u1780-\u17D3\u17D7\u17DC\u17DD\u17E0-\u17E9\u180B-\u180D\u1810-\u1819\u1820-\u1877\u1880-\u18AA\u18B0-\u18F5\u1900-\u191E\u1920-\u192B\u1930-\u193B\u1946-\u196D\u1970-\u1974\u1980-\u19AB\u19B0-\u19C9\u19D0-\u19DA\u1A00-\u1A1B\u1A20-\u1A5E\u1A60-\u1A7C\u1A7F-\u1A89\u1A90-\u1A99\u1AA7\u1AB0-\u1ABD\u1B00-\u1B4B\u1B50-\u1B59\u1B6B-\u1B73\u1B80-\u1BF3\u1C00-\u1C37\u1C40-\u1C49\u1C4D-\u1C7D\u1CD0-\u1CD2\u1CD4-\u1CF6\u1CF8\u1CF9\u1D00-\u1DF5\u1DFC-\u1F15\u1F18-\u1F1D\u1F20-\u1F45\u1F48-\u1F4D\u1F50-\u1F57\u1F59\u1F5B\u1F5D\u1F5F-\u1F7D\u1F80-\u1FB4\u1FB6-\u1FBC\u1FBE\u1FC2-\u1FC4\u1FC6-\u1FCC\u1FD0-\u1FD3\u1FD6-\u1FDB\u1FE0-\u1FEC\u1FF2-\u1FF4\u1FF6-\u1FFC\u200C\u200D\u203F\u2040\u2054\u2071\u207F\u2090-\u209C\u20D0-\u20DC\u20E1\u20E5-\u20F0\u2102\u2107\u210A-\u2113\u2115\u2118-\u211D\u2124\u2126\u2128\u212A-\u2139\u213C-\u213F\u2145-\u2149\u214E\u2160-\u2188\u2C00-\u2C2E\u2C30-\u2C5E\u2C60-\u2CE4\u2CEB-\u2CF3\u2D00-\u2D25\u2D27\u2D2D\u2D30-\u2D67\u2D6F\u2D7F-\u2D96\u2DA0-\u2DA6\u2DA8-\u2DAE\u2DB0-\u2DB6\u2DB8-\u2DBE\u2DC0-\u2DC6\u2DC8-\u2DCE\u2DD0-\u2DD6\u2DD8-\u2DDE\u2DE0-\u2DFF\u3005-\u3007\u3021-\u302F\u3031-\u3035\u3038-\u303C\u3041-\u3096\u3099-\u309F\u30A1-\u30FA\u30FC-\u30FF\u3105-\u312D\u3131-\u318E\u31A0-\u31BA\u31F0-\u31FF\u3400-\u4DB5\u4E00-\u9FD5\uA000-\uA48C\uA4D0-\uA4FD\uA500-\uA60C\uA610-\uA62B\uA640-\uA66F\uA674-\uA67D\uA67F-\uA6F1\uA717-\uA71F\uA722-\uA788\uA78B-\uA7AD\uA7B0-\uA7B7\uA7F7-\uA827\uA840-\uA873\uA880-\uA8C4\uA8D0-\uA8D9\uA8E0-\uA8F7\uA8FB\uA8FD\uA900-\uA92D\uA930-\uA953\uA960-\uA97C\uA980-\uA9C0\uA9CF-\uA9D9\uA9E0-\uA9FE\uAA00-\uAA36\uAA40-\uAA4D\uAA50-\uAA59\uAA60-\uAA76\uAA7A-\uAAC2\uAADB-\uAADD\uAAE0-\uAAEF\uAAF2-\uAAF6\uAB01-\uAB06\uAB09-\uAB0E\uAB11-\uAB16\uAB20-\uAB26\uAB28-\uAB2E\uAB30-\uAB5A\uAB5C-\uAB65\uAB70-\uABEA\uABEC\uABED\uABF0-\uABF9\uAC00-\uD7A3\uD7B0-\uD7C6\uD7CB-\uD7FB\uF900-\uFA6D\uFA70-\uFAD9\uFB00-\uFB06\uFB13-\uFB17\uFB1D-\uFB28\uFB2A-\uFB36\uFB38-\uFB3C\uFB3E\uFB40\uFB41\uFB43\uFB44\uFB46-\uFBB1\uFBD3-\uFD3D\uFD50-\uFD8F\uFD92-\uFDC7\uFDF0-\uFDFB\uFE00-\uFE0F\uFE20-\uFE2F\uFE33\uFE34\uFE4D-\uFE4F\uFE70-\uFE74\uFE76-\uFEFC\uFF10-\uFF19\uFF21-\uFF3A\uFF3F\uFF41-\uFF5A\uFF66-\uFFBE\uFFC2-\uFFC7\uFFCA-\uFFCF\uFFD2-\uFFD7\uFFDA-\uFFDC]|\uD800[\uDC00-\uDC0B\uDC0D-\uDC26\uDC28-\uDC3A\uDC3C\uDC3D\uDC3F-\uDC4D\uDC50-\uDC5D\uDC80-\uDCFA\uDD40-\uDD74\uDDFD\uDE80-\uDE9C\uDEA0-\uDED0\uDEE0\uDF00-\uDF1F\uDF30-\uDF4A\uDF50-\uDF7A\uDF80-\uDF9D\uDFA0-\uDFC3\uDFC8-\uDFCF\uDFD1-\uDFD5]|\uD801[\uDC00-\uDC9D\uDCA0-\uDCA9\uDD00-\uDD27\uDD30-\uDD63\uDE00-\uDF36\uDF40-\uDF55\uDF60-\uDF67]|\uD802[\uDC00-\uDC05\uDC08\uDC0A-\uDC35\uDC37\uDC38\uDC3C\uDC3F-\uDC55\uDC60-\uDC76\uDC80-\uDC9E\uDCE0-\uDCF2\uDCF4\uDCF5\uDD00-\uDD15\uDD20-\uDD39\uDD80-\uDDB7\uDDBE\uDDBF\uDE00-\uDE03\uDE05\uDE06\uDE0C-\uDE13\uDE15-\uDE17\uDE19-\uDE33\uDE38-\uDE3A\uDE3F\uDE60-\uDE7C\uDE80-\uDE9C\uDEC0-\uDEC7\uDEC9-\uDEE6\uDF00-\uDF35\uDF40-\uDF55\uDF60-\uDF72\uDF80-\uDF91]|\uD803[\uDC00-\uDC48\uDC80-\uDCB2\uDCC0-\uDCF2]|\uD804[\uDC00-\uDC46\uDC66-\uDC6F\uDC7F-\uDCBA\uDCD0-\uDCE8\uDCF0-\uDCF9\uDD00-\uDD34\uDD36-\uDD3F\uDD50-\uDD73\uDD76\uDD80-\uDDC4\uDDCA-\uDDCC\uDDD0-\uDDDA\uDDDC\uDE00-\uDE11\uDE13-\uDE37\uDE80-\uDE86\uDE88\uDE8A-\uDE8D\uDE8F-\uDE9D\uDE9F-\uDEA8\uDEB0-\uDEEA\uDEF0-\uDEF9\uDF00-\uDF03\uDF05-\uDF0C\uDF0F\uDF10\uDF13-\uDF28\uDF2A-\uDF30\uDF32\uDF33\uDF35-\uDF39\uDF3C-\uDF44\uDF47\uDF48\uDF4B-\uDF4D\uDF50\uDF57\uDF5D-\uDF63\uDF66-\uDF6C\uDF70-\uDF74]|\uD805[\uDC80-\uDCC5\uDCC7\uDCD0-\uDCD9\uDD80-\uDDB5\uDDB8-\uDDC0\uDDD8-\uDDDD\uDE00-\uDE40\uDE44\uDE50-\uDE59\uDE80-\uDEB7\uDEC0-\uDEC9\uDF00-\uDF19\uDF1D-\uDF2B\uDF30-\uDF39]|\uD806[\uDCA0-\uDCE9\uDCFF\uDEC0-\uDEF8]|\uD808[\uDC00-\uDF99]|\uD809[\uDC00-\uDC6E\uDC80-\uDD43]|[\uD80C\uD840-\uD868\uD86A-\uD86C\uD86F-\uD872][\uDC00-\uDFFF]|\uD80D[\uDC00-\uDC2E]|\uD811[\uDC00-\uDE46]|\uD81A[\uDC00-\uDE38\uDE40-\uDE5E\uDE60-\uDE69\uDED0-\uDEED\uDEF0-\uDEF4\uDF00-\uDF36\uDF40-\uDF43\uDF50-\uDF59\uDF63-\uDF77\uDF7D-\uDF8F]|\uD81B[\uDF00-\uDF44\uDF50-\uDF7E\uDF8F-\uDF9F]|\uD82C[\uDC00\uDC01]|\uD82F[\uDC00-\uDC6A\uDC70-\uDC7C\uDC80-\uDC88\uDC90-\uDC99\uDC9D\uDC9E]|\uD834[\uDD65-\uDD69\uDD6D-\uDD72\uDD7B-\uDD82\uDD85-\uDD8B\uDDAA-\uDDAD\uDE42-\uDE44]|\uD835[\uDC00-\uDC54\uDC56-\uDC9C\uDC9E\uDC9F\uDCA2\uDCA5\uDCA6\uDCA9-\uDCAC\uDCAE-\uDCB9\uDCBB\uDCBD-\uDCC3\uDCC5-\uDD05\uDD07-\uDD0A\uDD0D-\uDD14\uDD16-\uDD1C\uDD1E-\uDD39\uDD3B-\uDD3E\uDD40-\uDD44\uDD46\uDD4A-\uDD50\uDD52-\uDEA5\uDEA8-\uDEC0\uDEC2-\uDEDA\uDEDC-\uDEFA\uDEFC-\uDF14\uDF16-\uDF34\uDF36-\uDF4E\uDF50-\uDF6E\uDF70-\uDF88\uDF8A-\uDFA8\uDFAA-\uDFC2\uDFC4-\uDFCB\uDFCE-\uDFFF]|\uD836[\uDE00-\uDE36\uDE3B-\uDE6C\uDE75\uDE84\uDE9B-\uDE9F\uDEA1-\uDEAF]|\uD83A[\uDC00-\uDCC4\uDCD0-\uDCD6]|\uD83B[\uDE00-\uDE03\uDE05-\uDE1F\uDE21\uDE22\uDE24\uDE27\uDE29-\uDE32\uDE34-\uDE37\uDE39\uDE3B\uDE42\uDE47\uDE49\uDE4B\uDE4D-\uDE4F\uDE51\uDE52\uDE54\uDE57\uDE59\uDE5B\uDE5D\uDE5F\uDE61\uDE62\uDE64\uDE67-\uDE6A\uDE6C-\uDE72\uDE74-\uDE77\uDE79-\uDE7C\uDE7E\uDE80-\uDE89\uDE8B-\uDE9B\uDEA1-\uDEA3\uDEA5-\uDEA9\uDEAB-\uDEBB]|\uD869[\uDC00-\uDED6\uDF00-\uDFFF]|\uD86D[\uDC00-\uDF34\uDF40-\uDFFF]|\uD86E[\uDC00-\uDC1D\uDC20-\uDFFF]|\uD873[\uDC00-\uDEA1]|\uD87E[\uDC00-\uDE1D]|\uDB40[\uDD00-\uDDEF]/;
          k.Character = {
            fromCodePoint: function(a) {
              return 65536 > a ? String.fromCharCode(a) : String.fromCharCode(55296 + (a - 65536 >> 10)) + String.fromCharCode(56320 + (a - 65536 & 1023))
            },
            isWhiteSpace: function(a) {
              return 32 === a || 9 === a || 11 === a || 12 === a || 160 === a || 5760 <= a && 0 <= [5760, 8192, 8193, 8194, 8195, 8196, 8197, 8198, 8199, 8200, 8201, 8202, 8239, 8287, 12288, 65279].indexOf(a)
            },
            isLineTerminator: function(a) {
              return 10 === a || 13 === a || 8232 === a || 8233 === a
            },
            isIdentifierStart: function(a) {
              return 36 === a || 95 === a || 65 <= a && 90 >= a || 97 <= a && 122 >= a || 92 === a ||
                128 <= a && n.test(k.Character.fromCodePoint(a))
            },
            isIdentifierPart: function(a) {
              return 36 === a || 95 === a || 65 <= a && 90 >= a || 97 <= a && 122 >= a || 48 <= a && 57 >= a || 92 === a || 128 <= a && l.test(k.Character.fromCodePoint(a))
            },
            isDecimalDigit: function(a) {
              return 48 <= a && 57 >= a
            },
            isHexDigit: function(a) {
              return 48 <= a && 57 >= a || 65 <= a && 70 >= a || 97 <= a && 102 >= a
            },
            isOctalDigit: function(a) {
              return 48 <= a && 55 >= a
            }
          }
        }, function(c, k, n) {
          var l = n(2);
          c = function() {
            return function(a) {
              this.type = l.Syntax.ArrayExpression;
              this.elements = a
            }
          }();
          k.ArrayExpression = c;
          c = function() {
            return function(a) {
              this.type =
                l.Syntax.ArrayPattern;
              this.elements = a
            }
          }();
          k.ArrayPattern = c;
          c = function() {
            return function(a, c, h) {
              this.type = l.Syntax.ArrowFunctionExpression;
              this.id = null;
              this.params = a;
              this.body = c;
              this.generator = !1;
              this.expression = h
            }
          }();
          k.ArrowFunctionExpression = c;
          c = function() {
            return function(a, c, h) {
              this.type = l.Syntax.AssignmentExpression;
              this.operator = a;
              this.left = c;
              this.right = h
            }
          }();
          k.AssignmentExpression = c;
          c = function() {
            return function(a, c) {
              this.type = l.Syntax.AssignmentPattern;
              this.left = a;
              this.right = c
            }
          }();
          k.AssignmentPattern =
            c;
          c = function() {
            return function(a, c, h) {
              this.type = "||" === a || "&&" === a ? l.Syntax.LogicalExpression : l.Syntax.BinaryExpression;
              this.operator = a;
              this.left = c;
              this.right = h
            }
          }();
          k.BinaryExpression = c;
          c = function() {
            return function(a) {
              this.type = l.Syntax.BlockStatement;
              this.body = a
            }
          }();
          k.BlockStatement = c;
          c = function() {
            return function(a) {
              this.type = l.Syntax.BreakStatement;
              this.label = a
            }
          }();
          k.BreakStatement = c;
          c = function() {
            return function(a, c) {
              this.type = l.Syntax.CallExpression;
              this.callee = a;
              this.arguments = c
            }
          }();
          k.CallExpression =
            c;
          c = function() {
            return function(a, c) {
              this.type = l.Syntax.CatchClause;
              this.param = a;
              this.body = c
            }
          }();
          k.CatchClause = c;
          c = function() {
            return function(a) {
              this.type = l.Syntax.ClassBody;
              this.body = a
            }
          }();
          k.ClassBody = c;
          c = function() {
            return function(a, c, h) {
              this.type = l.Syntax.ClassDeclaration;
              this.id = a;
              this.superClass = c;
              this.body = h
            }
          }();
          k.ClassDeclaration = c;
          c = function() {
            return function(a, c, h) {
              this.type = l.Syntax.ClassExpression;
              this.id = a;
              this.superClass = c;
              this.body = h
            }
          }();
          k.ClassExpression = c;
          c = function() {
            return function(a,
              c) {
              this.type = l.Syntax.MemberExpression;
              this.computed = !0;
              this.object = a;
              this.property = c
            }
          }();
          k.ComputedMemberExpression = c;
          c = function() {
            return function(a, c, h) {
              this.type = l.Syntax.ConditionalExpression;
              this.test = a;
              this.consequent = c;
              this.alternate = h
            }
          }();
          k.ConditionalExpression = c;
          c = function() {
            return function(a) {
              this.type = l.Syntax.ContinueStatement;
              this.label = a
            }
          }();
          k.ContinueStatement = c;
          c = function() {
            return function() {
              this.type = l.Syntax.DebuggerStatement
            }
          }();
          k.DebuggerStatement = c;
          c = function() {
            return function(a,
              c) {
              this.type = l.Syntax.ExpressionStatement;
              this.expression = a;
              this.directive = c
            }
          }();
          k.Directive = c;
          c = function() {
            return function(a, c) {
              this.type = l.Syntax.DoWhileStatement;
              this.body = a;
              this.test = c
            }
          }();
          k.DoWhileStatement = c;
          c = function() {
            return function() {
              this.type = l.Syntax.EmptyStatement
            }
          }();
          k.EmptyStatement = c;
          c = function() {
            return function(a) {
              this.type = l.Syntax.ExportAllDeclaration;
              this.source = a
            }
          }();
          k.ExportAllDeclaration = c;
          c = function() {
            return function(a) {
              this.type = l.Syntax.ExportDefaultDeclaration;
              this.declaration =
                a
            }
          }();
          k.ExportDefaultDeclaration = c;
          c = function() {
            return function(a, c, h) {
              this.type = l.Syntax.ExportNamedDeclaration;
              this.declaration = a;
              this.specifiers = c;
              this.source = h
            }
          }();
          k.ExportNamedDeclaration = c;
          c = function() {
            return function(a, c) {
              this.type = l.Syntax.ExportSpecifier;
              this.exported = c;
              this.local = a
            }
          }();
          k.ExportSpecifier = c;
          c = function() {
            return function(a) {
              this.type = l.Syntax.ExpressionStatement;
              this.expression = a
            }
          }();
          k.ExpressionStatement = c;
          c = function() {
            return function(a, c, h) {
              this.type = l.Syntax.ForInStatement;
              this.left = a;
              this.right = c;
              this.body = h;
              this.each = !1
            }
          }();
          k.ForInStatement = c;
          c = function() {
            return function(a, c, h) {
              this.type = l.Syntax.ForOfStatement;
              this.left = a;
              this.right = c;
              this.body = h
            }
          }();
          k.ForOfStatement = c;
          c = function() {
            return function(a, c, h, k) {
              this.type = l.Syntax.ForStatement;
              this.init = a;
              this.test = c;
              this.update = h;
              this.body = k
            }
          }();
          k.ForStatement = c;
          c = function() {
            return function(a, c, h, k) {
              this.type = l.Syntax.FunctionDeclaration;
              this.id = a;
              this.params = c;
              this.body = h;
              this.generator = k;
              this.expression = !1
            }
          }();
          k.FunctionDeclaration =
            c;
          c = function() {
            return function(a, c, h, k) {
              this.type = l.Syntax.FunctionExpression;
              this.id = a;
              this.params = c;
              this.body = h;
              this.generator = k;
              this.expression = !1
            }
          }();
          k.FunctionExpression = c;
          c = function() {
            return function(a) {
              this.type = l.Syntax.Identifier;
              this.name = a
            }
          }();
          k.Identifier = c;
          c = function() {
            return function(a, c, h) {
              this.type = l.Syntax.IfStatement;
              this.test = a;
              this.consequent = c;
              this.alternate = h
            }
          }();
          k.IfStatement = c;
          c = function() {
            return function(a, c) {
              this.type = l.Syntax.ImportDeclaration;
              this.specifiers = a;
              this.source =
                c
            }
          }();
          k.ImportDeclaration = c;
          c = function() {
            return function(a) {
              this.type = l.Syntax.ImportDefaultSpecifier;
              this.local = a
            }
          }();
          k.ImportDefaultSpecifier = c;
          c = function() {
            return function(a) {
              this.type = l.Syntax.ImportNamespaceSpecifier;
              this.local = a
            }
          }();
          k.ImportNamespaceSpecifier = c;
          c = function() {
            return function(a, c) {
              this.type = l.Syntax.ImportSpecifier;
              this.local = a;
              this.imported = c
            }
          }();
          k.ImportSpecifier = c;
          c = function() {
            return function(a, c) {
              this.type = l.Syntax.LabeledStatement;
              this.label = a;
              this.body = c
            }
          }();
          k.LabeledStatement =
            c;
          c = function() {
            return function(a, c) {
              this.type = l.Syntax.Literal;
              this.value = a;
              this.raw = c
            }
          }();
          k.Literal = c;
          c = function() {
            return function(a, c) {
              this.type = l.Syntax.MetaProperty;
              this.meta = a;
              this.property = c
            }
          }();
          k.MetaProperty = c;
          c = function() {
            return function(a, c, h, k, e) {
              this.type = l.Syntax.MethodDefinition;
              this.key = a;
              this.computed = c;
              this.value = h;
              this.kind = k;
              this["static"] = e
            }
          }();
          k.MethodDefinition = c;
          c = function() {
            return function(a, c) {
              this.type = l.Syntax.NewExpression;
              this.callee = a;
              this.arguments = c
            }
          }();
          k.NewExpression =
            c;
          c = function() {
            return function(a) {
              this.type = l.Syntax.ObjectExpression;
              this.properties = a
            }
          }();
          k.ObjectExpression = c;
          c = function() {
            return function(a) {
              this.type = l.Syntax.ObjectPattern;
              this.properties = a
            }
          }();
          k.ObjectPattern = c;
          c = function() {
            return function(a, c) {
              this.type = l.Syntax.Program;
              this.body = a;
              this.sourceType = c
            }
          }();
          k.Program = c;
          c = function() {
            return function(a, c, h, k, e, g) {
              this.type = l.Syntax.Property;
              this.key = c;
              this.computed = h;
              this.value = k;
              this.kind = a;
              this.method = e;
              this.shorthand = g
            }
          }();
          k.Property = c;
          c = function() {
            return function(a,
              c, h) {
              this.type = l.Syntax.Literal;
              this.value = a;
              this.raw = c;
              this.regex = h
            }
          }();
          k.RegexLiteral = c;
          c = function() {
            return function(a) {
              this.type = l.Syntax.RestElement;
              this.argument = a
            }
          }();
          k.RestElement = c;
          c = function() {
            return function(a) {
              this.type = l.Syntax.ReturnStatement;
              this.argument = a
            }
          }();
          k.ReturnStatement = c;
          c = function() {
            return function(a) {
              this.type = l.Syntax.SequenceExpression;
              this.expressions = a
            }
          }();
          k.SequenceExpression = c;
          c = function() {
            return function(a) {
              this.type = l.Syntax.SpreadElement;
              this.argument = a
            }
          }();
          k.SpreadElement =
            c;
          c = function() {
            return function(a, c) {
              this.type = l.Syntax.MemberExpression;
              this.computed = !1;
              this.object = a;
              this.property = c
            }
          }();
          k.StaticMemberExpression = c;
          c = function() {
            return function() {
              this.type = l.Syntax.Super
            }
          }();
          k.Super = c;
          c = function() {
            return function(a, c) {
              this.type = l.Syntax.SwitchCase;
              this.test = a;
              this.consequent = c
            }
          }();
          k.SwitchCase = c;
          c = function() {
            return function(a, c) {
              this.type = l.Syntax.SwitchStatement;
              this.discriminant = a;
              this.cases = c
            }
          }();
          k.SwitchStatement = c;
          c = function() {
            return function(a, c) {
              this.type =
                l.Syntax.TaggedTemplateExpression;
              this.tag = a;
              this.quasi = c
            }
          }();
          k.TaggedTemplateExpression = c;
          c = function() {
            return function(a, c) {
              this.type = l.Syntax.TemplateElement;
              this.value = a;
              this.tail = c
            }
          }();
          k.TemplateElement = c;
          c = function() {
            return function(a, c) {
              this.type = l.Syntax.TemplateLiteral;
              this.quasis = a;
              this.expressions = c
            }
          }();
          k.TemplateLiteral = c;
          c = function() {
            return function() {
              this.type = l.Syntax.ThisExpression
            }
          }();
          k.ThisExpression = c;
          c = function() {
            return function(a) {
              this.type = l.Syntax.ThrowStatement;
              this.argument =
                a
            }
          }();
          k.ThrowStatement = c;
          c = function() {
            return function(a, c, h) {
              this.type = l.Syntax.TryStatement;
              this.block = a;
              this.handler = c;
              this.finalizer = h
            }
          }();
          k.TryStatement = c;
          c = function() {
            return function(a, c) {
              this.type = l.Syntax.UnaryExpression;
              this.operator = a;
              this.argument = c;
              this.prefix = !0
            }
          }();
          k.UnaryExpression = c;
          c = function() {
            return function(a, c, h) {
              this.type = l.Syntax.UpdateExpression;
              this.operator = a;
              this.argument = c;
              this.prefix = h
            }
          }();
          k.UpdateExpression = c;
          c = function() {
            return function(a, c) {
              this.type = l.Syntax.VariableDeclaration;
              this.declarations = a;
              this.kind = c
            }
          }();
          k.VariableDeclaration = c;
          c = function() {
            return function(a, c) {
              this.type = l.Syntax.VariableDeclarator;
              this.id = a;
              this.init = c
            }
          }();
          k.VariableDeclarator = c;
          c = function() {
            return function(a, c) {
              this.type = l.Syntax.WhileStatement;
              this.test = a;
              this.body = c
            }
          }();
          k.WhileStatement = c;
          c = function() {
            return function(a, c) {
              this.type = l.Syntax.WithStatement;
              this.object = a;
              this.body = c
            }
          }();
          k.WithStatement = c;
          c = function() {
            return function(a, c) {
              this.type = l.Syntax.YieldExpression;
              this.argument = a;
              this.delegate =
                c
            }
          }();
          k.YieldExpression = c
        }, function(c, k, n) {
          function l(a) {
            switch (a.type) {
              case e.JSXSyntax.JSXIdentifier:
                var b = a.name;
                break;
              case e.JSXSyntax.JSXNamespacedName:
                b = l(a.namespace) + ":" + l(a.name);
                break;
              case e.JSXSyntax.JSXMemberExpression:
                b = l(a.object) + "." + l(a.property)
            }
            return b
          }
          var a = this && this.__extends || function(a, b) {
              function e() {
                this.constructor = a
              }
              for (var d in b) b.hasOwnProperty(d) && (a[d] = b[d]);
              a.prototype = null === b ? Object.create(b) : (e.prototype = b.prototype, new e)
            },
            m = n(9),
            h = n(7);
          c = n(3);
          var q = n(12),
            e = n(13),
            g = n(10),
            f = n(14),
            b;
          (function(a) {
            a[a.Identifier = 100] = "Identifier";
            a[a.Text = 101] = "Text"
          })(b || (b = {}));
          h.TokenName[b.Identifier] = "JSXIdentifier";
          h.TokenName[b.Text] = "JSXText";
          n = function(d) {
            function c(a, b, c) {
              d.call(this, a, b, c)
            }
            a(c, d);
            c.prototype.parsePrimaryExpression = function() {
              return this.match("<") ? this.parseJSXRoot() : d.prototype.parsePrimaryExpression.call(this)
            };
            c.prototype.startJSX = function() {
              this.scanner.index = this.startMarker.index;
              this.scanner.lineNumber = this.startMarker.lineNumber;
              this.scanner.lineStart =
                this.startMarker.lineStart
            };
            c.prototype.finishJSX = function() {
              this.nextToken()
            };
            c.prototype.reenterJSX = function() {
              this.startJSX();
              this.expectJSX("}");
              this.config.tokens && this.tokens.pop()
            };
            c.prototype.createJSXNode = function() {
              this.collectComments();
              return {
                index: this.scanner.index,
                line: this.scanner.lineNumber,
                column: this.scanner.index - this.scanner.lineStart
              }
            };
            c.prototype.createJSXChildNode = function() {
              return {
                index: this.scanner.index,
                line: this.scanner.lineNumber,
                column: this.scanner.index - this.scanner.lineStart
              }
            };
            c.prototype.scanXHTMLEntity = function(a) {
              for (var b = "&", c = !0, e = !1, d = !1, f = !1; !this.scanner.eof() && c && !e;) {
                var g = this.scanner.source[this.scanner.index];
                if (g === a) break;
                e = ";" === g;
                b += g;
                ++this.scanner.index;
                if (!e) switch (b.length) {
                  case 2:
                    d = "#" === g;
                    break;
                  case 3:
                    d && (c = (f = "x" === g) || m.Character.isDecimalDigit(g.charCodeAt(0)), d = d && !f);
                    break;
                  default:
                    c = (c = c && !(d && !m.Character.isDecimalDigit(g.charCodeAt(0)))) && !(f && !m.Character.isHexDigit(g.charCodeAt(0)))
                }
              }
              c && e && 2 < b.length && (a = b.substr(1, b.length - 2), d && 1 < a.length ?
                b = String.fromCharCode(parseInt(a.substr(1), 10)) : f && 2 < a.length ? b = String.fromCharCode(parseInt("0" + a.substr(1), 16)) : d || f || !q.XHTMLEntities[a] || (b = q.XHTMLEntities[a]));
              return b
            };
            c.prototype.lexJSX = function() {
              var a = this.scanner.source.charCodeAt(this.scanner.index);
              if (60 === a || 62 === a || 47 === a || 58 === a || 61 === a || 123 === a || 125 === a) {
                var c = this.scanner.source[this.scanner.index++];
                return {
                  type: h.Token.Punctuator,
                  value: c,
                  lineNumber: this.scanner.lineNumber,
                  lineStart: this.scanner.lineStart,
                  start: this.scanner.index -
                    1,
                  end: this.scanner.index
                }
              }
              if (34 === a || 39 === a) {
                a = this.scanner.index;
                c = this.scanner.source[this.scanner.index++];
                for (var e = ""; !this.scanner.eof();) {
                  var d = this.scanner.source[this.scanner.index++];
                  if (d === c) break;
                  else e = "&" === d ? e + this.scanXHTMLEntity(c) : e + d
                }
                return {
                  type: h.Token.StringLiteral,
                  value: e,
                  lineNumber: this.scanner.lineNumber,
                  lineStart: this.scanner.lineStart,
                  start: a,
                  end: this.scanner.index
                }
              }
              if (46 === a) return a = this.scanner.source.charCodeAt(this.scanner.index + 1), c = this.scanner.source.charCodeAt(this.scanner.index +
                2), c = 46 === a && 46 === c ? "..." : ".", a = this.scanner.index, this.scanner.index += c.length, {
                type: h.Token.Punctuator,
                value: c,
                lineNumber: this.scanner.lineNumber,
                lineStart: this.scanner.lineStart,
                start: a,
                end: this.scanner.index
              };
              if (96 === a) return {
                type: h.Token.Template,
                lineNumber: this.scanner.lineNumber,
                lineStart: this.scanner.lineStart,
                start: this.scanner.index,
                end: this.scanner.index
              };
              if (m.Character.isIdentifierStart(a) && 92 !== a) {
                a = this.scanner.index;
                for (++this.scanner.index; !this.scanner.eof();)
                  if (d = this.scanner.source.charCodeAt(this.scanner.index),
                    m.Character.isIdentifierPart(d) && 92 !== d) ++this.scanner.index;
                  else if (45 === d) ++this.scanner.index;
                else break;
                c = this.scanner.source.slice(a, this.scanner.index);
                return {
                  type: b.Identifier,
                  value: c,
                  lineNumber: this.scanner.lineNumber,
                  lineStart: this.scanner.lineStart,
                  start: a,
                  end: this.scanner.index
                }
              }
              this.scanner.throwUnexpectedToken()
            };
            c.prototype.nextJSXToken = function() {
              this.collectComments();
              this.startMarker.index = this.scanner.index;
              this.startMarker.lineNumber = this.scanner.lineNumber;
              this.startMarker.lineStart =
                this.scanner.lineStart;
              var a = this.lexJSX();
              this.lastMarker.index = this.scanner.index;
              this.lastMarker.lineNumber = this.scanner.lineNumber;
              this.lastMarker.lineStart = this.scanner.lineStart;
              this.config.tokens && this.tokens.push(this.convertToken(a));
              return a
            };
            c.prototype.nextJSXText = function() {
              this.startMarker.index = this.scanner.index;
              this.startMarker.lineNumber = this.scanner.lineNumber;
              this.startMarker.lineStart = this.scanner.lineStart;
              for (var a = this.scanner.index, c = ""; !this.scanner.eof();) {
                var e = this.scanner.source[this.scanner.index];
                if ("{" === e || "<" === e) break;
                ++this.scanner.index;
                c += e;
                m.Character.isLineTerminator(e.charCodeAt(0)) && (++this.scanner.lineNumber, "\r" === e && "\n" === this.scanner.source[this.scanner.index] && ++this.scanner.index, this.scanner.lineStart = this.scanner.index)
              }
              this.lastMarker.index = this.scanner.index;
              this.lastMarker.lineNumber = this.scanner.lineNumber;
              this.lastMarker.lineStart = this.scanner.lineStart;
              a = {
                type: b.Text,
                value: c,
                lineNumber: this.scanner.lineNumber,
                lineStart: this.scanner.lineStart,
                start: a,
                end: this.scanner.index
              };
              0 < c.length && this.config.tokens && this.tokens.push(this.convertToken(a));
              return a
            };
            c.prototype.peekJSXToken = function() {
              var a = this.scanner.index,
                b = this.scanner.lineNumber,
                c = this.scanner.lineStart;
              this.scanner.scanComments();
              var e = this.lexJSX();
              this.scanner.index = a;
              this.scanner.lineNumber = b;
              this.scanner.lineStart = c;
              return e
            };
            c.prototype.expectJSX = function(a) {
              var b = this.nextJSXToken();
              b.type === h.Token.Punctuator && b.value === a || this.throwUnexpectedToken(b)
            };
            c.prototype.matchJSX = function(a) {
              var b = this.peekJSXToken();
              return b.type === h.Token.Punctuator && b.value === a
            };
            c.prototype.parseJSXIdentifier = function() {
              var a = this.createJSXNode(),
                c = this.nextJSXToken();
              c.type !== b.Identifier && this.throwUnexpectedToken(c);
              return this.finalize(a, new f.JSXIdentifier(c.value))
            };
            c.prototype.parseJSXElementName = function() {
              var a = this.createJSXNode(),
                b = this.parseJSXIdentifier();
              if (this.matchJSX(":")) {
                this.expectJSX(":");
                var c = this.parseJSXIdentifier();
                b = this.finalize(a, new f.JSXNamespacedName(b, c))
              } else if (this.matchJSX("."))
                for (; this.matchJSX(".");) this.expectJSX("."),
                  c = this.parseJSXIdentifier(), b = this.finalize(a, new f.JSXMemberExpression(b, c));
              return b
            };
            c.prototype.parseJSXAttributeName = function() {
              var a = this.createJSXNode(),
                b = this.parseJSXIdentifier();
              if (this.matchJSX(":")) {
                this.expectJSX(":");
                var c = this.parseJSXIdentifier();
                a = this.finalize(a, new f.JSXNamespacedName(b, c))
              } else a = b;
              return a
            };
            c.prototype.parseJSXStringLiteralAttribute = function() {
              var a = this.createJSXNode(),
                b = this.nextJSXToken();
              b.type !== h.Token.StringLiteral && this.throwUnexpectedToken(b);
              var c = this.getTokenRaw(b);
              return this.finalize(a, new g.Literal(b.value, c))
            };
            c.prototype.parseJSXExpressionAttribute = function() {
              var a = this.createJSXNode();
              this.expectJSX("{");
              this.finishJSX();
              this.match("}") && this.tolerateError("JSX attributes must only be assigned a non-empty expression");
              var b = this.parseAssignmentExpression();
              this.reenterJSX();
              return this.finalize(a, new f.JSXExpressionContainer(b))
            };
            c.prototype.parseJSXAttributeValue = function() {
              return this.matchJSX("{") ? this.parseJSXExpressionAttribute() : this.matchJSX("<") ?
                this.parseJSXElement() : this.parseJSXStringLiteralAttribute()
            };
            c.prototype.parseJSXNameValueAttribute = function() {
              var a = this.createJSXNode(),
                b = this.parseJSXAttributeName(),
                c = null;
              this.matchJSX("=") && (this.expectJSX("="), c = this.parseJSXAttributeValue());
              return this.finalize(a, new f.JSXAttribute(b, c))
            };
            c.prototype.parseJSXSpreadAttribute = function() {
              var a = this.createJSXNode();
              this.expectJSX("{");
              this.expectJSX("...");
              this.finishJSX();
              var b = this.parseAssignmentExpression();
              this.reenterJSX();
              return this.finalize(a,
                new f.JSXSpreadAttribute(b))
            };
            c.prototype.parseJSXAttributes = function() {
              for (var a = []; !this.matchJSX("/") && !this.matchJSX(">");) {
                var b = this.matchJSX("{") ? this.parseJSXSpreadAttribute() : this.parseJSXNameValueAttribute();
                a.push(b)
              }
              return a
            };
            c.prototype.parseJSXOpeningElement = function() {
              var a = this.createJSXNode();
              this.expectJSX("<");
              var b = this.parseJSXElementName(),
                c = this.parseJSXAttributes(),
                e = this.matchJSX("/");
              e && this.expectJSX("/");
              this.expectJSX(">");
              return this.finalize(a, new f.JSXOpeningElement(b,
                e, c))
            };
            c.prototype.parseJSXBoundaryElement = function() {
              var a = this.createJSXNode();
              this.expectJSX("<");
              if (this.matchJSX("/")) {
                this.expectJSX("/");
                var b = this.parseJSXElementName();
                this.expectJSX(">");
                return this.finalize(a, new f.JSXClosingElement(b))
              }
              b = this.parseJSXElementName();
              var c = this.parseJSXAttributes(),
                e = this.matchJSX("/");
              e && this.expectJSX("/");
              this.expectJSX(">");
              return this.finalize(a, new f.JSXOpeningElement(b, e, c))
            };
            c.prototype.parseJSXEmptyExpression = function() {
              var a = this.createJSXChildNode();
              this.collectComments();
              this.lastMarker.index = this.scanner.index;
              this.lastMarker.lineNumber = this.scanner.lineNumber;
              this.lastMarker.lineStart = this.scanner.lineStart;
              return this.finalize(a, new f.JSXEmptyExpression)
            };
            c.prototype.parseJSXExpressionContainer = function() {
              var a = this.createJSXNode();
              this.expectJSX("{");
              if (this.matchJSX("}")) {
                var b = this.parseJSXEmptyExpression();
                this.expectJSX("}")
              } else this.finishJSX(), b = this.parseAssignmentExpression(), this.reenterJSX();
              return this.finalize(a, new f.JSXExpressionContainer(b))
            };
            c.prototype.parseJSXChildren = function() {
              for (var a = []; !this.scanner.eof();) {
                var b = this.createJSXChildNode(),
                  c = this.nextJSXText();
                if (c.start < c.end) {
                  var e = this.getTokenRaw(c);
                  b = this.finalize(b, new f.JSXText(c.value, e));
                  a.push(b)
                }
                if ("{" === this.scanner.source[this.scanner.index]) b = this.parseJSXExpressionContainer(), a.push(b);
                else break
              }
              return a
            };
            c.prototype.parseComplexJSXElement = function(a) {
              for (var b = []; !this.scanner.eof();) {
                a.children = a.children.concat(this.parseJSXChildren());
                var c = this.createJSXChildNode(),
                  d = this.parseJSXBoundaryElement();
                if (d.type === e.JSXSyntax.JSXOpeningElement) {
                  var g = d;
                  g.selfClosing ? (c = this.finalize(c, new f.JSXElement(g, [], null)), a.children.push(c)) : (b.push(a), a = {
                    node: c,
                    opening: g,
                    closing: null,
                    children: []
                  })
                }
                if (d.type === e.JSXSyntax.JSXClosingElement)
                  if (a.closing = d, d = l(a.opening.name), c = l(a.closing.name), d !== c && this.tolerateError("Expected corresponding JSX closing tag for %0", d), 0 < b.length) c = this.finalize(a.node, new f.JSXElement(a.opening, a.children, a.closing)), a = b.pop(), a.children.push(c);
                  else break
              }
              return a
            };
            c.prototype.parseJSXElement = function() {
              var a = this.createJSXNode(),
                b = this.parseJSXOpeningElement(),
                c = [],
                e = null;
              b.selfClosing || (e = this.parseComplexJSXElement({
                node: a,
                opening: b,
                closing: e,
                children: c
              }), c = e.children, e = e.closing);
              return this.finalize(a, new f.JSXElement(b, c, e))
            };
            c.prototype.parseJSXRoot = function() {
              this.config.tokens && this.tokens.pop();
              this.startJSX();
              var a = this.parseJSXElement();
              this.finishJSX();
              return a
            };
            return c
          }(c.Parser);
          k.JSXParser = n
        }, function(c, k) {
          k.XHTMLEntities = {
            quot: '"',
            amp: "&",
            apos: "'",
            gt: ">",
            nbsp: "\u00a0",
            iexcl: "\u00a1",
            cent: "\u00a2",
            pound: "\u00a3",
            curren: "\u00a4",
            yen: "\u00a5",
            brvbar: "\u00a6",
            sect: "\u00a7",
            uml: "\u00a8",
            copy: "\u00a9",
            ordf: "\u00aa",
            laquo: "\u00ab",
            not: "\u00ac",
            shy: "\u00ad",
            reg: "\u00ae",
            macr: "\u00af",
            deg: "\u00b0",
            plusmn: "\u00b1",
            sup2: "\u00b2",
            sup3: "\u00b3",
            acute: "\u00b4",
            micro: "\u00b5",
            para: "\u00b6",
            middot: "\u00b7",
            cedil: "\u00b8",
            sup1: "\u00b9",
            ordm: "\u00ba",
            raquo: "\u00bb",
            frac14: "\u00bc",
            frac12: "\u00bd",
            frac34: "\u00be",
            iquest: "\u00bf",
            Agrave: "\u00c0",
            Aacute: "\u00c1",
            Acirc: "\u00c2",
            Atilde: "\u00c3",
            Auml: "\u00c4",
            Aring: "\u00c5",
            AElig: "\u00c6",
            Ccedil: "\u00c7",
            Egrave: "\u00c8",
            Eacute: "\u00c9",
            Ecirc: "\u00ca",
            Euml: "\u00cb",
            Igrave: "\u00cc",
            Iacute: "\u00cd",
            Icirc: "\u00ce",
            Iuml: "\u00cf",
            ETH: "\u00d0",
            Ntilde: "\u00d1",
            Ograve: "\u00d2",
            Oacute: "\u00d3",
            Ocirc: "\u00d4",
            Otilde: "\u00d5",
            Ouml: "\u00d6",
            times: "\u00d7",
            Oslash: "\u00d8",
            Ugrave: "\u00d9",
            Uacute: "\u00da",
            Ucirc: "\u00db",
            Uuml: "\u00dc",
            Yacute: "\u00dd",
            THORN: "\u00de",
            szlig: "\u00df",
            agrave: "\u00e0",
            aacute: "\u00e1",
            acirc: "\u00e2",
            atilde: "\u00e3",
            auml: "\u00e4",
            aring: "\u00e5",
            aelig: "\u00e6",
            ccedil: "\u00e7",
            egrave: "\u00e8",
            eacute: "\u00e9",
            ecirc: "\u00ea",
            euml: "\u00eb",
            igrave: "\u00ec",
            iacute: "\u00ed",
            icirc: "\u00ee",
            iuml: "\u00ef",
            eth: "\u00f0",
            ntilde: "\u00f1",
            ograve: "\u00f2",
            oacute: "\u00f3",
            ocirc: "\u00f4",
            otilde: "\u00f5",
            ouml: "\u00f6",
            divide: "\u00f7",
            oslash: "\u00f8",
            ugrave: "\u00f9",
            uacute: "\u00fa",
            ucirc: "\u00fb",
            uuml: "\u00fc",
            yacute: "\u00fd",
            thorn: "\u00fe",
            yuml: "\u00ff",
            OElig: "\u0152",
            oelig: "\u0153",
            Scaron: "\u0160",
            scaron: "\u0161",
            Yuml: "\u0178",
            fnof: "\u0192",
            circ: "\u02c6",
            tilde: "\u02dc",
            Alpha: "\u0391",
            Beta: "\u0392",
            Gamma: "\u0393",
            Delta: "\u0394",
            Epsilon: "\u0395",
            Zeta: "\u0396",
            Eta: "\u0397",
            Theta: "\u0398",
            Iota: "\u0399",
            Kappa: "\u039a",
            Lambda: "\u039b",
            Mu: "\u039c",
            Nu: "\u039d",
            Xi: "\u039e",
            Omicron: "\u039f",
            Pi: "\u03a0",
            Rho: "\u03a1",
            Sigma: "\u03a3",
            Tau: "\u03a4",
            Upsilon: "\u03a5",
            Phi: "\u03a6",
            Chi: "\u03a7",
            Psi: "\u03a8",
            Omega: "\u03a9",
            alpha: "\u03b1",
            beta: "\u03b2",
            gamma: "\u03b3",
            delta: "\u03b4",
            epsilon: "\u03b5",
            zeta: "\u03b6",
            eta: "\u03b7",
            theta: "\u03b8",
            iota: "\u03b9",
            kappa: "\u03ba",
            lambda: "\u03bb",
            mu: "\u03bc",
            nu: "\u03bd",
            xi: "\u03be",
            omicron: "\u03bf",
            pi: "\u03c0",
            rho: "\u03c1",
            sigmaf: "\u03c2",
            sigma: "\u03c3",
            tau: "\u03c4",
            upsilon: "\u03c5",
            phi: "\u03c6",
            chi: "\u03c7",
            psi: "\u03c8",
            omega: "\u03c9",
            thetasym: "\u03d1",
            upsih: "\u03d2",
            piv: "\u03d6",
            ensp: "\u2002",
            emsp: "\u2003",
            thinsp: "\u2009",
            zwnj: "\u200c",
            zwj: "\u200d",
            lrm: "\u200e",
            rlm: "\u200f",
            ndash: "\u2013",
            mdash: "\u2014",
            lsquo: "\u2018",
            rsquo: "\u2019",
            sbquo: "\u201a",
            ldquo: "\u201c",
            rdquo: "\u201d",
            bdquo: "\u201e",
            dagger: "\u2020",
            Dagger: "\u2021",
            bull: "\u2022",
            hellip: "\u2026",
            permil: "\u2030",
            prime: "\u2032",
            Prime: "\u2033",
            lsaquo: "\u2039",
            rsaquo: "\u203a",
            oline: "\u203e",
            frasl: "\u2044",
            euro: "\u20ac",
            image: "\u2111",
            weierp: "\u2118",
            real: "\u211c",
            trade: "\u2122",
            alefsym: "\u2135",
            larr: "\u2190",
            uarr: "\u2191",
            rarr: "\u2192",
            darr: "\u2193",
            harr: "\u2194",
            crarr: "\u21b5",
            lArr: "\u21d0",
            uArr: "\u21d1",
            rArr: "\u21d2",
            dArr: "\u21d3",
            hArr: "\u21d4",
            forall: "\u2200",
            part: "\u2202",
            exist: "\u2203",
            empty: "\u2205",
            nabla: "\u2207",
            isin: "\u2208",
            notin: "\u2209",
            ni: "\u220b",
            prod: "\u220f",
            sum: "\u2211",
            minus: "\u2212",
            lowast: "\u2217",
            radic: "\u221a",
            prop: "\u221d",
            infin: "\u221e",
            ang: "\u2220",
            and: "\u2227",
            or: "\u2228",
            cap: "\u2229",
            cup: "\u222a",
            "int": "\u222b",
            there4: "\u2234",
            sim: "\u223c",
            cong: "\u2245",
            asymp: "\u2248",
            ne: "\u2260",
            equiv: "\u2261",
            le: "\u2264",
            ge: "\u2265",
            sub: "\u2282",
            sup: "\u2283",
            nsub: "\u2284",
            sube: "\u2286",
            supe: "\u2287",
            oplus: "\u2295",
            otimes: "\u2297",
            perp: "\u22a5",
            sdot: "\u22c5",
            lceil: "\u2308",
            rceil: "\u2309",
            lfloor: "\u230a",
            rfloor: "\u230b",
            loz: "\u25ca",
            spades: "\u2660",
            clubs: "\u2663",
            hearts: "\u2665",
            diams: "\u2666",
            lang: "\u27e8",
            rang: "\u27e9"
          }
        }, function(c, k) {
          k.JSXSyntax = {
            JSXAttribute: "JSXAttribute",
            JSXClosingElement: "JSXClosingElement",
            JSXElement: "JSXElement",
            JSXEmptyExpression: "JSXEmptyExpression",
            JSXExpressionContainer: "JSXExpressionContainer",
            JSXIdentifier: "JSXIdentifier",
            JSXMemberExpression: "JSXMemberExpression",
            JSXNamespacedName: "JSXNamespacedName",
            JSXOpeningElement: "JSXOpeningElement",
            JSXSpreadAttribute: "JSXSpreadAttribute",
            JSXText: "JSXText"
          }
        }, function(c, k, n) {
          var l = n(13);
          c = function() {
            return function(a) {
              this.type = l.JSXSyntax.JSXClosingElement;
              this.name = a
            }
          }();
          k.JSXClosingElement = c;
          c = function() {
            return function(a, c, h) {
              this.type = l.JSXSyntax.JSXElement;
              this.openingElement = a;
              this.children = c;
              this.closingElement = h
            }
          }();
          k.JSXElement = c;
          c = function() {
            return function() {
              this.type = l.JSXSyntax.JSXEmptyExpression
            }
          }();
          k.JSXEmptyExpression = c;
          c = function() {
            return function(a) {
              this.type = l.JSXSyntax.JSXExpressionContainer;
              this.expression = a
            }
          }();
          k.JSXExpressionContainer = c;
          c = function() {
            return function(a) {
              this.type = l.JSXSyntax.JSXIdentifier;
              this.name = a
            }
          }();
          k.JSXIdentifier = c;
          c = function() {
            return function(a, c) {
              this.type = l.JSXSyntax.JSXMemberExpression;
              this.object = a;
              this.property = c
            }
          }();
          k.JSXMemberExpression = c;
          c = function() {
            return function(a, c) {
              this.type = l.JSXSyntax.JSXAttribute;
              this.name = a;
              this.value = c
            }
          }();
          k.JSXAttribute = c;
          c = function() {
            return function(a, c) {
              this.type = l.JSXSyntax.JSXNamespacedName;
              this.namespace = a;
              this.name = c
            }
          }();
          k.JSXNamespacedName =
            c;
          c = function() {
            return function(a, c, h) {
              this.type = l.JSXSyntax.JSXOpeningElement;
              this.name = a;
              this.selfClosing = c;
              this.attributes = h
            }
          }();
          k.JSXOpeningElement = c;
          c = function() {
            return function(a) {
              this.type = l.JSXSyntax.JSXSpreadAttribute;
              this.argument = a
            }
          }();
          k.JSXSpreadAttribute = c;
          c = function() {
            return function(a, c) {
              this.type = l.JSXSyntax.JSXText;
              this.value = a;
              this.raw = c
            }
          }();
          k.JSXText = c
        }, function(c, k, n) {
          var l = n(8),
            a = n(6),
            m = n(7),
            h = function() {
              function a() {
                this.values = [];
                this.curly = this.paren = -1
              }
              a.prototype.beforeFunctionExpression =
                function(a) {
                  return 0 <= "( { [ in typeof instanceof new return case delete throw void = += -= *= **= /= %= <<= >>= >>>= &= |= ^= , + - * ** / % ++ -- << >> >>> & | ^ ! ~ && || ? : === == >= <= < > != !==".split(" ").indexOf(a)
                };
              a.prototype.isRegexStart = function() {
                var a = this.values[this.values.length - 1],
                  c = null !== a;
                switch (a) {
                  case "this":
                  case "]":
                    c = !1;
                    break;
                  case ")":
                    a = this.values[this.paren - 1];
                    c = "if" === a || "while" === a || "for" === a || "with" === a;
                    break;
                  case "}":
                    c = !1, "function" === this.values[this.curly - 3] ? c = (a =
                      this.values[this.curly - 4]) ? !this.beforeFunctionExpression(a) : !1 : "function" === this.values[this.curly - 4] && (c = (a = this.values[this.curly - 5]) ? !this.beforeFunctionExpression(a) : !0)
                }
                return c
              };
              a.prototype.push = function(a) {
                a.type === m.Token.Punctuator || a.type === m.Token.Keyword ? ("{" === a.value ? this.curly = this.values.length : "(" === a.value && (this.paren = this.values.length), this.values.push(a.value)) : this.values.push(null)
              };
              return a
            }();
          c = function() {
            function c(c, g) {
              this.errorHandler = new a.ErrorHandler;
              this.errorHandler.tolerant =
                g ? "boolean" === typeof g.tolerant && g.tolerant : !1;
              this.scanner = new l.Scanner(c, this.errorHandler);
              this.scanner.trackComment = g ? "boolean" === typeof g.comment && g.comment : !1;
              this.trackRange = g ? "boolean" === typeof g.range && g.range : !1;
              this.trackLoc = g ? "boolean" === typeof g.loc && g.loc : !1;
              this.buffer = [];
              this.reader = new h
            }
            c.prototype.errors = function() {
              return this.errorHandler.errors
            };
            c.prototype.getNextToken = function() {
              if (0 === this.buffer.length) {
                var a = this.scanner.scanComments();
                if (this.scanner.trackComment)
                  for (var c =
                      0; c < a.length; ++c) {
                    var f = a[c];
                    var b = this.scanner.source.slice(f.slice[0], f.slice[1]);
                    b = {
                      type: f.multiLine ? "BlockComment" : "LineComment",
                      value: b
                    };
                    this.trackRange && (b.range = f.range);
                    this.trackLoc && (b.loc = f.loc);
                    this.buffer.push(b)
                  }
                this.scanner.eof() || (a = void 0, this.trackLoc && (a = {
                    start: {
                      line: this.scanner.lineNumber,
                      column: this.scanner.index - this.scanner.lineStart
                    },
                    end: {}
                  }), c = "/" === this.scanner.source[this.scanner.index] ? this.reader.isRegexStart() ? this.scanner.scanRegExp() : this.scanner.scanPunctuator() :
                  this.scanner.lex(), this.reader.push(c), f = {
                    type: m.TokenName[c.type],
                    value: this.scanner.source.slice(c.start, c.end)
                  }, this.trackRange && (f.range = [c.start, c.end]), this.trackLoc && (a.end = {
                    line: this.scanner.lineNumber,
                    column: this.scanner.index - this.scanner.lineStart
                  }, f.loc = a), c.regex && (f.regex = c.regex), this.buffer.push(f))
              }
              return this.buffer.shift()
            };
            return c
          }();
          k.Tokenizer = c
        }])
      })
  }, {}]
}, {}, [1]);
