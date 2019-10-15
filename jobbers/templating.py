import jinja2    # http://jinja.pocoo.org/docs/2.10/


def render_to_out(job, output):
    """ render a dict "job".
        Returns number of bytes written.
    """
    with open(job.template) as file_:

        template = jinja2.Template(file_.read())

        o = template.render(job=job, template=job.template)

        return output.write(o)
