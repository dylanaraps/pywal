# Gets theme information for fish shell completions.
#
# Usage: crystal contrib/tools/get_themes.cr

def get(name)
  Dir.children("pywal/colorschemes/#{name}").map do |file|
    file.chomp(".json")
  end
end

light  = get("light")
dark   = get("dark")
themes = light.dup.concat(dark).uniq

result = String.build do |str|
  themes.each do |theme|
    n = 0
    n += 1 if light.includes?(theme)
    n += 2 if dark.includes?(theme)

    description = case n
    when 1
      "Light theme"
    when 2
      "Dark theme"
    when 3
      "Light and dark theme"
    end

    str << "#{theme}\\t'#{description}'\n"
  end
end

print result
