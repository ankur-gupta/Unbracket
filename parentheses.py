import sublime
import sublime_plugin


class RemoveParenthesesCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        selection = self.view.sel()
        region = selection[0]
        line = self.view.line(region)
        string = self.view.substr(line)
        print('region =', region)
        print('line =', line)
        print('string =', string)

        # Bracket specification
        bracket = '()'

        # Quote specification
        quote = '"'

        # Search for first occurrence of bracket start
        quote_active = False
        for index, character in enumerate(string):
            if character == quote:
                quote_active = not quote_active
                continue
            if quote_active:
                continue
            if character == bracket[0]:
                parentheses_start_index = index
                break
            else:
                parentheses_start_index = None

        if parentheses_start_index is None:
            print('No starting parentheses found. Nothing to do.')
            return

        print('parentheses_start_index =', parentheses_start_index)
        print('string[parentheses_start_index] =',
              string[parentheses_start_index])

        # Finding the end parentheses is very difficult and
        # requires parsing the code manually a bit.
        assert parentheses_start_index < len(string)
        parentheses_end_index = None
        count = 1
        quote_active = False
        for index in range(parentheses_start_index + 1, len(string)):
            if string[index] == quote:
                quote_active = not quote_active
                continue
            if quote_active:
                continue
            if string[index] == bracket[0]:
                count = count + 1
            if string[index] == bracket[1]:
                count = count - 1
            if count == 0:
                parentheses_end_index = index
                break

        if parentheses_end_index is None:
            print('Cannot find ending parentheses. Nothing to do.')
            return

        print('parentheses_end_index =', parentheses_end_index)
        print('string[parentheses_end_index] =', string[parentheses_end_index])

        # Determine outside region start and end
        outside_region_start = region.a
        outside_region_end = line.a + parentheses_end_index + 1
        assert outside_region_start <= outside_region_end
        outside_region = sublime.Region(outside_region_start,
                                        outside_region_end)
        outside_string = self.view.substr(outside_region)
        print('outside_string =', outside_string)

        # Determine inside region start and end
        inside_region_start = line.a + parentheses_start_index + 1
        inside_region_end = line.a + parentheses_end_index
        assert inside_region_start <= inside_region_end
        inside_region = sublime.Region(inside_region_start, inside_region_end)
        inside_string = self.view.substr(inside_region)
        print('inside_string =', inside_string)

        self.view.replace(edit, outside_region, inside_string)
        # self.view.insert(edit, 0, "{}\n".format(inside_string))

