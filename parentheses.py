import sublime
import sublime_plugin


class UnbracketCommand(sublime_plugin.TextCommand):
    # Bracket specifications
    brackets = ['()', '[]', '{}']

    # Quote specifications
    quotes = ['"', "'"]

    def _get_operating_region(self):
        region = self.view.sel()[0]
        if region.a == region.b:
            line = self.view.line(region)
            operating_region = sublime.Region(region.a, line.b)
        else:
            operating_region = region

        # Ensure operating region is valid
        if operating_region.a > operating_region.b:
            operating_region = sublime.Region(operating_region.b,
                                              operating_region.a)
        return operating_region

    def _find_bracket_open_position(self, string):
        ''' Search for first occurrence of bracket start of any kind '''
        qoutes = {qoute: False for qoute in self.quotes}
        for index, character in enumerate(string):
            if character in qoutes:
                qoutes[character] = not qoutes[character]
                continue
            if any([active for active in qoutes.values()]):
                continue
            for bracket in self.brackets:
                if character == bracket[0]:
                    return (index, bracket)
        return (None, None)

    def _find_bracket_close_position(self, string,
                                     bracket_open_position, bracket):
        ''' Search for the matching bracket close position '''
        assert bracket_open_position < len(string)
        bracket_close_position = None
        count = 1
        qoutes = {qoute: False for qoute in self.quotes}
        for index in range(bracket_open_position + 1, len(string)):
            if string[index] in qoutes:
                qoutes[string[index]] = not qoutes[string[index]]
                continue
            if any([active for active in qoutes.values()]):
                continue
            if string[index] == bracket[0]:
                count = count + 1
            if string[index] == bracket[1]:
                count = count - 1
            if count == 0:
                bracket_close_position = index
                break
        return bracket_close_position

    def _get_region_to_be_replaced(self, operating_region,
                                   bracket_close_position):
        ''' Determine the region that needs to be replaced '''
        region_to_be_replaced = sublime.Region(
            operating_region.a,
            operating_region.a + bracket_close_position + 1
        )
        return region_to_be_replaced

    def _get_string_to_replace_with(self, operating_region,
                                    bracket_open_position,
                                    bracket_close_position):
        ''' Compute the string that to replace with '''
        start = operating_region.a + bracket_open_position + 1
        end = operating_region.a + bracket_close_position
        assert start <= end
        region_to_replace_with = sublime.Region(start, end)
        string_to_replace_with = self.view.substr(region_to_replace_with)
        return string_to_replace_with

    def run(self, edit):
        operating_region = self._get_operating_region()
        operating_string = self.view.substr(operating_region)
        bracket_open_position, bracket = \
            self._find_bracket_open_position(operating_string)

        if bracket_open_position is None:
            print('Cannot find bracket open position. Exiting!')
            return

        bracket_close_position = \
            self._find_bracket_close_position(operating_string,
                                              bracket_open_position,
                                              bracket)

        # Hard part is done.
        region_to_be_replaced = \
            self._get_region_to_be_replaced(operating_region,
                                            bracket_close_position)
        string_to_replace_with = \
            self._get_string_to_replace_with(operating_region,
                                             bracket_open_position,
                                             bracket_close_position)

        # Replace
        self.view.replace(edit, region_to_be_replaced, string_to_replace_with)


    # def run(self, edit):
    #     selection = self.view.sel()
    #     region = selection[0]
    #     line = self.view.line(region)
    #     string = self.view.substr(line)
    #     print('region =', region)
    #     print('line =', line)
    #     print('string =', string)

    #     # Search for first occurrence of bracket start of any kind.
    #     brackets = {bracket: False for bracket in BRACKETS}
    #     brackets_open = [bracket[0] for bracket in brackets.iterkeys()]
    #     qoutes = {qoute: False for qoute in QUOTES}
    #     for index, character in enumerate(string):
    #         if character in qoutes:
    #             qoutes[character] = not qoutes[character]
    #             continue
    #         if any([active for active in qoutes.values()]):
    #             continue
    #         if character in brackets_open:
    #             bracket = brackets_open
    #             parentheses_start_index = index
    #             break
    #         else:
    #             parentheses_start_index = None

    #     if parentheses_start_index is None:
    #         print('No starting parentheses found. Nothing to do.')
    #         return

    #     print('parentheses_start_index =', parentheses_start_index)
    #     print('string[parentheses_start_index] =',
    #           string[parentheses_start_index])

    #     # Finding the end parentheses is very difficult and
    #     # requires parsing the code manually a bit.
    #     assert parentheses_start_index < len(string)
    #     parentheses_end_index = None
    #     count = 1
    #     qoutes = {qoute: False for qoute in QUOTES}
    #     for index in range(parentheses_start_index + 1, len(string)):
    #         if string[index] in qoutes:
    #             qoutes[string[index]] = not qoutes[string[index]]
    #             continue
    #         if any([active for active in qoutes.values()]):
    #             continue
    #         if string[index] == bracket[0]:
    #             count = count + 1
    #         if string[index] == bracket[1]:
    #             count = count - 1
    #         if count == 0:
    #             parentheses_end_index = index
    #             break

    #     if parentheses_end_index is None:
    #         print('Cannot find ending parentheses. Nothing to do.')
    #         return

    #     print('parentheses_end_index =', parentheses_end_index)
    #     print('string[parentheses_end_index] =', string[parentheses_end_index])

    #     # Determine outside region start and end
    #     outside_region_start = region.a
    #     outside_region_end = line.a + parentheses_end_index + 1
    #     assert outside_region_start <= outside_region_end
    #     outside_region = sublime.Region(outside_region_start,
    #                                     outside_region_end)
    #     outside_string = self.view.substr(outside_region)
    #     print('outside_string =', outside_string)

    #     # Determine inside region start and end
    #     inside_region_start = line.a + parentheses_start_index + 1
    #     inside_region_end = line.a + parentheses_end_index
    #     assert inside_region_start <= inside_region_end
    #     inside_region = sublime.Region(inside_region_start, inside_region_end)
    #     inside_string = self.view.substr(inside_region)
    #     print('inside_string =', inside_string)

    #     self.view.replace(edit, outside_region, inside_string)
    #     # self.view.insert(edit, 0, "{}\n".format(inside_string))

