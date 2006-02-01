#!C:/usr/ruby/bin/ruby.exe
#
# trpy
#

require 'cgi'
require 'erb'
require 'yaml'

class DataPool
  def initialize(data_dir)
    @data_dir = data_dir
    @entries = entries
  end

  def entries
    Dir.glob("#{@data_dir}/*").map{|e| File.basename(e) }
  end

  def random_page
    @entries[rand(@entries.size)]
  end

  def new_page_id
    id = nil
    while true
      id = rand(100000000).to_s
      break unless @entries.include?(id)
    end
    id
  end
end


config = YAML.load_file("./trpy.conf")
trpy_url = config["trpy_url"]
template_dir = config["template_dir"]
data_dir = config["data_dir"]
pool = DataPool.new(data_dir)
cgi = CGI.new
if cgi.include?('c')
  template = "#{template_dir}/create.rhtml"
  page_body = ""
elsif cgi.include?('e')
  template = "#{template_dir}/edit.rhtml"
  page_id = cgi.params['e'][0]
  data = File.open("#{data_dir}/#{page_id}", "r"){|f| f.readlines}
  page_body = data.join("")
elsif cgi.include?('u')
  template = "#{template_dir}/trpy.rhtml"
  page_id = cgi.params['u'][0] == "" ? pool.new_page_id : cgi.params['u'][0]
  data = CGI.escapeHTML(CGI.unescape(cgi.params['content'][0]))
  File.open("#{data_dir}/#{page_id}", "wb"){|f| f.write(data)}
  data = data.split("\n")
  page_title = data.shift.chomp
  page_body = data.map{|l| l.chomp}.join("<br />\n")
else
  template = "#{template_dir}/trpy.rhtml"
  page_id = pool.random_page
  data = File.open("#{data_dir}/#{page_id}", "r"){|f| f.readlines}
  page_title = data.shift.chomp
  page_body = data.map{|l| l.chomp}.join("<br />\n")
end

print "Content-type: text/html\n\n"
page = ERB.new(File.open(template){|f| f.read}, nil, "<>")
page.run

